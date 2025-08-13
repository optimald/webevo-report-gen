#!/usr/bin/env python3
"""
WebEvo.ai Website Scanning & Report Generation System

This script monitors the reports-raw directory for new JSON files and automatically
generates professional PDF reports with WebEvo.ai branding.
"""

import json
import os
import sys
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.parse import urlparse

import click
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jinja2 import Environment, FileSystemLoader, Template
from playwright.sync_api import sync_playwright
import dateutil.parser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('webevo_reports.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """Handles the generation of WebEvo.ai reports from JSON scan data."""
    
    def __init__(self, template_dir: str = "templates", output_dir: str = "reports-final"):
        self.template_dir = Path(template_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=True
        )
        
        # Load the HTML template
        self.template = self._load_template()
        
    def _load_template(self) -> Template:
        """Load the HTML template for report generation."""
        try:
            # First try to load from templates directory
            if (self.template_dir / "report_template.html").exists():
                return self.jinja_env.get_template("report_template.html")
            
            # Fallback to existing aisav.com.html
            template_path = Path("aisav.com.html")
            if template_path.exists():
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                return Template(template_content)
            else:
                raise FileNotFoundError("No template file found")
                
        except Exception as e:
            logger.error(f"Failed to load template: {e}")
            raise
    
    def parse_json_data(self, json_file_path: str) -> Dict[str, Any]:
        """Parse and validate JSON scan data."""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate required fields
            required_fields = ['url', 'generatedAt', 'overallScore', 'overallRating']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Parse and format the data
            parsed_data = {
                'url': data['url'],
                'generatedAt': data['generatedAt'],
                'overallScore': data['overallScore'],
                'overallRating': data['overallRating'],
                'modules': data.get('modules', {}),
                'topRecommendations': data.get('topRecommendations', {}),
                'reportId': data.get('reportId', ''),
                'schemaVersion': data.get('schemaVersion', ''),
                'industryContext': data.get('industryContext', {}),
                'viewports': data.get('viewports', [])
            }
            
            logger.info(f"Successfully parsed JSON data for {parsed_data['url']}")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Failed to parse JSON data from {json_file_path}: {e}")
            raise
    
    def generate_html(self, data: Dict[str, Any]) -> str:
        """Generate HTML content from template and data."""
        try:
            # Format the generation date
            if data['generatedAt']:
                try:
                    gen_date = dateutil.parser.parse(data['generatedAt'])
                    data['formattedDate'] = gen_date.strftime('%B %d, %Y')
                except:
                    data['formattedDate'] = data['generatedAt']
            
            # Extract domain from URL for filename
            parsed_url = urlparse(data['url'])
            data['domain'] = parsed_url.netloc.replace('www.', '')
            
            # Render the template
            html_content = self.template.render(**data)
            logger.info(f"Generated HTML for {data['url']}")
            return html_content
            
        except Exception as e:
            logger.error(f"Failed to generate HTML: {e}")
            raise
    
    def generate_pdf(self, html_content: str, output_filename: str) -> str:
        """Generate PDF from HTML content using Playwright."""
        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # Set content and wait for it to load
                page.set_content(html_content, wait_until='networkidle')
                
                # Wait for any dynamic content to render
                time.sleep(2)
                
                # Generate PDF with full height (no pagination)
                pdf_path = self.output_dir / output_filename
                page.pdf(
                    path=str(pdf_path),
                    format='A4',
                    print_background=True,
                    prefer_css_page_size=True,
                    margin={
                        'top': '0.5in',
                        'right': '0.5in',
                        'bottom': '0.5in',
                        'left': '0.5in'
                    }
                )
                
                browser.close()
                
                logger.info(f"Generated PDF: {pdf_path}")
                return str(pdf_path)
                
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            raise
    
    def generate_report(self, json_file_path: str) -> Optional[str]:
        """Generate a complete report from JSON file."""
        try:
            # Parse JSON data
            data = self.parse_json_data(json_file_path)
            
            # Generate HTML
            html_content = self.generate_html(data)
            
            # Create output filename
            parsed_url = urlparse(data['url'])
            domain = parsed_url.netloc.replace('www.', '').replace('.', '-')
            
            # Parse date for filename
            try:
                gen_date = dateutil.parser.parse(data['generatedAt'])
                date_str = gen_date.strftime('%Y-%m-%d')
            except:
                date_str = datetime.now().strftime('%Y-%m-%d')
            
            output_filename = f"{domain}_{date_str}_webevo-ai.pdf"
            
            # Generate PDF
            pdf_path = self.generate_pdf(html_content, output_filename)
            
            logger.info(f"Successfully generated report: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            logger.error(f"Failed to generate report from {json_file_path}: {e}")
            return None

class FileWatcher(FileSystemEventHandler):
    """Monitors directory for new JSON files and triggers report generation."""
    
    def __init__(self, report_generator: ReportGenerator):
        self.report_generator = report_generator
        self.processed_files = set()
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix.lower() == '.json':
            self._process_file(file_path)
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix.lower() == '.json':
            self._process_file(file_path)
    
    def _process_file(self, file_path: Path):
        """Process a JSON file for report generation."""
        if str(file_path) in self.processed_files:
            return
        
        logger.info(f"Processing new file: {file_path}")
        
        try:
            # Wait a moment to ensure file is fully written
            time.sleep(1)
            
            # Generate report
            result = self.report_generator.generate_report(str(file_path))
            
            if result:
                self.processed_files.add(str(file_path))
                logger.info(f"Successfully processed {file_path}")
            else:
                logger.error(f"Failed to process {file_path}")
                
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

def watch_directory(watch_dir: str, report_generator: ReportGenerator):
    """Start watching directory for new files."""
    event_handler = FileWatcher(report_generator)
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=False)
    observer.start()
    
    logger.info(f"Started watching directory: {watch_dir}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Stopped watching directory")
    
    observer.join()

@click.command()
@click.option('--watch', 'watch_dir', default='reports-raw', 
              help='Directory to watch for new JSON files')
@click.option('--output', 'output_dir', default='reports-final',
              help='Directory to save generated reports')
@click.option('--template', 'template_dir', default='templates',
              help='Directory containing HTML templates')
@click.option('--single', 'single_file', 
              help='Process a single JSON file instead of watching directory')
def main(watch_dir: str, output_dir: str, template_dir: str, single_file: str):
    """WebEvo.ai Report Generator - Generate professional reports from scan data."""
    
    try:
        # Initialize report generator
        report_generator = ReportGenerator(template_dir, output_dir)
        
        if single_file:
            # Process single file
            logger.info(f"Processing single file: {single_file}")
            result = report_generator.generate_report(single_file)
            if result:
                logger.info(f"Report generated successfully: {result}")
            else:
                logger.error("Failed to generate report")
                sys.exit(1)
        else:
            # Watch directory for new files
            logger.info("Starting file watcher...")
            watch_directory(watch_dir, report_generator)
            
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
