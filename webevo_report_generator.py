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
            
            # Fix the items conflict by renaming to avoid Jinja2 .items() method confusion
            if 'topRecommendations' in parsed_data and 'items' in parsed_data['topRecommendations']:
                parsed_data['topRecommendations']['recommendations_list'] = parsed_data['topRecommendations'].pop('items')
            
            # Fix module recommendations items conflict
            if 'modules' in parsed_data:
                for module_key, module in parsed_data['modules'].items():
                    if 'recommendations' in module and 'items' in module['recommendations']:
                        module['recommendations']['recommendations_list'] = module['recommendations'].pop('items')
                    if 'issues' in module and 'items' in module['issues']:
                        module['issues']['issues_list'] = module['issues'].pop('items')
            
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
            
            # Add helper data for template
            data['overallGrade'] = self._get_grade(data['overallScore'])
            data['moduleGrade'] = {}
            data['moduleIcons'] = self._get_module_icons()
            data['moduleDescriptions'] = self._get_module_descriptions()
            
            # Calculate grades for each module
            if 'modules' in data:
                for module_key, module in data['modules'].items():
                    if 'summary' in module and 'score' in module['summary']:
                        data['moduleGrade'][module_key] = self._get_grade(module['summary']['score'])
            
            # Render the template
            html_content = self.template.render(**data)
            logger.info(f"Generated HTML for {data['url']}")
            return html_content
            
        except Exception as e:
            logger.error(f"Failed to generate HTML: {e}")
            raise
    
    def _get_grade(self, score: int) -> str:
        """Convert numeric score to letter grade."""
        if score >= 97:
            return 'A+'
        elif score >= 93:
            return 'A'
        elif score >= 90:
            return 'A-'
        elif score >= 87:
            return 'B+'
        elif score >= 83:
            return 'B'
        elif score >= 80:
            return 'B-'
        elif score >= 77:
            return 'C+'
        elif score >= 73:
            return 'C'
        elif score >= 70:
            return 'C-'
        elif score >= 67:
            return 'D+'
        elif score >= 63:
            return 'D'
        elif score >= 60:
            return 'D-'
        else:
            return 'F'
    
    def _get_module_icons(self) -> Dict[str, str]:
        """Get module icons for the template."""
        return {
            'ui': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0-4.4-3.6-8-8-8s-8 3.6-8 8c0 2 .8 3.8 2.2 5.2Z"/><path d="M7 17a5 5 0 0 0 10 0"/><path d="M12 22v-3"/><path d="M2 12h3"/><path d="M19 12h3"/></svg>',
            'performance': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 12-4-4-4 4"/><path d="m18 12v6a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-6"/><path d="m2 12 4 4 4-4"/><path d="m6 12V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v6"/></svg>',
            'seoContent': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
            'security': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
            'privacy': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>',
            'compatibility': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"></rect><line x1="2" y1="10" x2="22" y2="10"></line></svg>',
            'marketing': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
            'conversion': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v10l-4-4"/><path d="m16 6-4 4"/><path d="M20.4 13.4A9 9 0 1 1 10.6 4.6"/></svg>',
            'accessibility': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>'
        }
    
    def _get_module_descriptions(self) -> Dict[str, str]:
        """Get module descriptions for the template."""
        return {
            'ui': 'Analyzes the visual design, layout, and branding. A strong UI creates a professional, trustworthy impression.',
            'performance': 'Measures website speed and responsiveness. Faster sites provide a better user experience and rank higher in search results.',
            'seoContent': 'Evaluates how well the site is optimized for search engines. Good SEO helps potential customers find your website.',
            'security': 'Checks for vulnerabilities and proper security configurations. Strong security protects your business and your customers.',
            'privacy': 'Assesses data handling practices and privacy policies. Proper privacy is crucial for legal compliance and building user trust.',
            'compatibility': 'Tests how the website functions across different browsers and devices. Broad compatibility ensures a consistent experience for all visitors.',
            'marketing': 'Reviews online marketing elements like social media and calls-to-action. Effective marketing turns visitors into customers.',
            'conversion': 'Analyzes how effectively the site encourages visitors to take action. A high conversion rate means the website is successful at generating business.',
            'accessibility': 'Checks if the website is usable by people with disabilities. Accessibility is often a legal requirement and expands your potential audience.'
        }
    
    def generate_png(self, html_content: str, output_filename: str) -> str:
        """Generate PNG screenshot from HTML content using Playwright."""
        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Set content and wait for it to load
                page.set_content(html_content, wait_until='networkidle')
                
                # Wait for JavaScript to execute and populate content
                try:
                    # Wait for opportunities to be populated (more reliable than signal)
                    page.wait_for_selector('#opportunities-list > div', timeout=15000)
                    logger.info("Opportunities detected, proceeding with screenshot")
                except Exception as e:
                    logger.warning(f"Opportunities not detected: {e}, trying warnings...")
                    try:
                        # Fallback: wait for warnings
                        page.wait_for_selector('#warnings-list > div', timeout=10000)
                        logger.info("Warnings detected, proceeding with screenshot")
                    except Exception as e2:
                        logger.warning(f"Warnings not detected: {e2}, using fixed delay")
                        time.sleep(5)
                
                # Additional delay to ensure rendering is complete
                time.sleep(2)
                
                # Generate PNG screenshot with full page height
                page.screenshot(
                    path=output_filename,
                    full_page=True,  # Capture entire page height
                    type='png'
                )
                browser.close()
                
                logger.info(f"Generated PNG: {output_filename}")
                return output_filename
                
        except Exception as e:
            logger.error(f"Failed to generate PNG: {e}")
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
            
            # Generate output filename
            output_filename = f"{domain}_{date_str}_webevo-ai.png"
            
            # Generate PNG
            png_path = self.generate_png(html_content, output_filename)
            
            logger.info(f"Successfully generated report: {png_path}")
            return str(png_path)
            
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
