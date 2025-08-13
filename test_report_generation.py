#!/usr/bin/env python3
"""
Test script for WebEvo.ai Report Generator

This script tests the report generation functionality with sample data.
"""

import json
import tempfile
import os
from pathlib import Path
from webevo_report_generator import ReportGenerator

def create_test_data():
    """Create sample JSON data for testing."""
    return {
        "reportId": "test-123",
        "url": "https://test-website.com/",
        "generatedAt": "2025-08-13T10:00:00.000Z",
        "overallScore": 78,
        "overallRating": "Good",
        "modules": {
            "ui": {
                "summary": {
                    "score": 85,
                    "rating": "Good"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Improve mobile responsiveness by implementing a flexible grid system"
                        },
                        {
                            "text": "Enhance accessibility with better focus indicators"
                        }
                    ]
                }
            },
            "performance": {
                "summary": {
                    "score": 72,
                    "rating": "Needs Work"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Optimize image loading with lazy loading"
                        },
                        {
                            "text": "Minimize render-blocking resources"
                        }
                    ]
                }
            },
            "security": {
                "summary": {
                    "score": 90,
                    "rating": "Excellent"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Maintain current security configuration"
                        }
                    ]
                }
            }
        },
        "topRecommendations": {
            "items": [
                {
                    "text": "Focus on mobile optimization for better user experience"
                },
                {
                    "text": "Implement performance improvements for faster loading"
                }
            ]
        }
    }

def test_report_generation():
    """Test the complete report generation process."""
    print("🧪 Testing WebEvo.ai Report Generator...")
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create test directories
        test_output = temp_path / "test-output"
        test_output.mkdir()
        
        # Create test JSON file
        test_json = temp_path / "test-data.json"
        test_data = create_test_data()
        
        with open(test_json, 'w') as f:
            json.dump(test_data, f, indent=2)
        
        print(f"✅ Created test data: {test_json}")
        
        try:
            # Initialize report generator
            generator = ReportGenerator(
                template_dir="templates",
                output_dir=str(test_output)
            )
            
            print("✅ Initialized report generator")
            
            # Generate report
            result = generator.generate_report(str(test_json))
            
            if result:
                print(f"✅ Report generated successfully: {result}")
                
                # Check if file exists
                if os.path.exists(result):
                    file_size = os.path.getsize(result)
                    print(f"✅ PDF file created: {file_size} bytes")
                    
                    # List output directory
                    output_files = list(test_output.glob("*.pdf"))
                    print(f"✅ Output directory contains {len(output_files)} PDF files:")
                    for pdf_file in output_files:
                        print(f"   - {pdf_file.name}")
                else:
                    print("❌ PDF file not found")
                    return False
            else:
                print("❌ Report generation failed")
                return False
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            return False
    
    print("🎉 All tests passed!")
    return True

def test_single_file_processing():
    """Test processing a single file."""
    print("\n🔍 Testing single file processing...")
    
    # Use existing JSON file if available
    existing_json = Path("reports-raw/2025-08-13_02-19-34-900Z_eastmountaindental-com_6323faea.json")
    
    if existing_json.exists():
        print(f"✅ Found existing JSON file: {existing_json}")
        
        try:
            # Initialize generator
            generator = ReportGenerator()
            
            # Generate report
            result = generator.generate_report(str(existing_json))
            
            if result:
                print(f"✅ Report generated: {result}")
                return True
            else:
                print("❌ Report generation failed")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    else:
        print("ℹ️  No existing JSON file found for testing")
        return True

if __name__ == "__main__":
    print("🚀 WebEvo.ai Report Generator - Test Suite")
    print("=" * 50)
    
    # Test 1: Basic functionality with sample data
    test1_passed = test_report_generation()
    
    # Test 2: Process existing file if available
    test2_passed = test_single_file_processing()
    
    print("\n" + "=" * 50)
    if test1_passed and test2_passed:
        print("🎉 All tests passed! The system is working correctly.")
        print("\nNext steps:")
        print("1. Run: python webevo_report_generator.py")
        print("2. Add JSON files to reports-raw/ directory")
        print("3. Check reports-final/ for generated PDFs")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed")
        print("2. Check that Playwright is properly installed")
        print("3. Verify template files exist")
        print("4. Check file permissions")
