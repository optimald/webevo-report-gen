#!/usr/bin/env python3
"""
Demo script for WebEvo.ai Report Generator

This script demonstrates the report generation capabilities with sample data.
"""

import json
import os
from pathlib import Path
from webevo_report_generator import ReportGenerator

def create_demo_data():
    """Create comprehensive demo data for showcasing the system."""
    return {
        "reportId": "demo-2025-001",
        "url": "https://demo-website.com/",
        "generatedAt": "2025-08-13T14:30:00.000Z",
        "overallScore": 82,
        "overallRating": "Good",
        "schemaVersion": "3.11.0",
        "tier": "Professional",
        "modules": {
            "ui": {
                "summary": {
                    "score": 88,
                    "rating": "Good"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Implement responsive typography system using CSS custom properties for consistent mobile and desktop layouts"
                        },
                        {
                            "text": "Enhance accessibility by implementing clear focus states and improving semantic HTML markup"
                        },
                        {
                            "text": "Optimize brand consistency by creating a precise design system with standardized color palette"
                        }
                    ]
                }
            },
            "performance": {
                "summary": {
                    "score": 75,
                    "rating": "Needs Work"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Optimize image loading by implementing lazy loading and compressing images to reduce initial page load time"
                        },
                        {
                            "text": "Minimize render-blocking JavaScript and CSS by deferring non-critical scripts and inlining critical CSS"
                        },
                        {
                            "text": "Enable browser caching and implement a content delivery network (CDN) to reduce server response times"
                        }
                    ]
                }
            },
            "seoContent": {
                "summary": {
                    "score": 92,
                    "rating": "Excellent"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Continue maintaining high-quality, keyword-rich content that addresses user search intent"
                        },
                        {
                            "text": "Consider expanding content with more long-tail keywords for better niche targeting"
                        }
                    ]
                }
            },
            "security": {
                "summary": {
                    "score": 85,
                    "rating": "Good"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Implement comprehensive CSP with strict source restrictions for enhanced security"
                        },
                        {
                            "text": "Add X-Frame-Options: DENY or SAMEORIGIN to prevent clickjacking attacks"
                        }
                    ]
                }
            },
            "privacy": {
                "summary": {
                    "score": 78,
                    "rating": "Underperforming"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Enhance privacy policy with specific compliance details and clearer data handling practices"
                        },
                        {
                            "text": "Implement more granular consent management for better user control"
                        }
                    ]
                }
            },
            "compatibility": {
                "summary": {
                    "score": 90,
                    "rating": "Excellent"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Maintain current excellent cross-browser and device compatibility standards"
                        }
                    ]
                }
            },
            "marketing": {
                "summary": {
                    "score": 70,
                    "rating": "Needs Work"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Optimize call-to-action elements by improving button design and using action-oriented language"
                        },
                        {
                            "text": "Strengthen brand consistency by standardizing visual elements and messaging tone"
                        }
                    ]
                }
            },
            "conversion": {
                "summary": {
                    "score": 68,
                    "rating": "Needs Work"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Optimize form design by reducing field count and improving mobile experience"
                        },
                        {
                            "text": "Implement A/B testing for different conversion funnel variations"
                        }
                    ]
                }
            },
            "accessibility": {
                "summary": {
                    "score": 85,
                    "rating": "Good"
                },
                "recommendations": {
                    "items": [
                        {
                            "text": "Add descriptive alt text to images without alternative text"
                        },
                        {
                            "text": "Improve keyboard navigation and focus management"
                        }
                    ]
                }
            }
        },
        "topRecommendations": {
            "items": [
                {
                    "text": "Focus on performance optimization to improve user experience and search engine rankings"
                },
                {
                    "text": "Enhance conversion optimization through better form design and user experience"
                },
                {
                    "text": "Strengthen privacy compliance and data handling transparency"
                }
            ]
        },
        "industryContext": {
            "primaryIndustry": "Technology",
            "subtype": "Software Services",
            "confidence": 95
        }
    }

def run_demo():
    """Run the complete demo."""
    print("🎭 WebEvo.ai Report Generator - Demo Mode")
    print("=" * 50)
    
    # Create demo data
    demo_data = create_demo_data()
    
    # Create demo JSON file
    demo_file = Path("demo-data.json")
    with open(demo_file, 'w') as f:
        json.dump(demo_data, f, indent=2)
    
    print(f"✅ Created demo data file: {demo_file}")
    print(f"🌐 Website: {demo_data['url']}")
    print(f"📊 Overall Score: {demo_data['overallScore']}/100 ({demo_data['overallRating']})")
    print(f"📋 Modules: {len(demo_data['modules'])} categories analyzed")
    
    # Initialize report generator
    print("\n🔧 Initializing report generator...")
    generator = ReportGenerator()
    
    # Generate report
    print("📄 Generating demo report...")
    result = generator.generate_report(str(demo_file))
    
    if result:
        print(f"✅ Demo report generated successfully!")
        print(f"📁 Location: {result}")
        
        # Check file size
        if os.path.exists(result):
            file_size = os.path.getsize(result)
            print(f"📏 File size: {file_size:,} bytes")
        
        # List generated files
        output_dir = Path("reports-final")
        if output_dir.exists():
            pdf_files = list(output_dir.glob("*.pdf"))
            print(f"📚 Total reports in output directory: {len(pdf_files)}")
            
            if pdf_files:
                print("📋 Generated reports:")
                for pdf_file in sorted(pdf_files, key=lambda x: x.stat().st_mtime, reverse=True):
                    print(f"   • {pdf_file.name}")
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Next steps:")
        print("1. Open the generated PDF to see the report")
        print("2. Try adding your own JSON files to 'reports-raw/'")
        print("3. Run: python webevo_report_generator.py")
        print("4. Check 'reports-final/' for automatically generated reports")
        
    else:
        print("❌ Demo report generation failed")
        return False
    
    # Clean up demo file
    if demo_file.exists():
        demo_file.unlink()
        print(f"🧹 Cleaned up demo file: {demo_file}")
    
    return True

if __name__ == "__main__":
    try:
        success = run_demo()
        if success:
            print("\n🚀 Ready to generate real reports!")
        else:
            print("\n⚠️  Demo had issues. Check the logs for details.")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check the installation and try again.")
