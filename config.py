"""
Configuration and helper functions for WebEvo.ai Report Generator
"""

import re
from typing import Dict, Any

# Module icons for the template
MODULE_ICONS = {
    'ui': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0-4.4-3.6-8-8-8s-8 3.6-8 8c0 2 .8 3.8 2.2 5.2Z"/><path d="M7 17a5 5 0 0 0 10 0"/><path d="M12 22v-3"/><path d="M2 12h3"/><path d="M19 12h3"/></svg>',
    'performance': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 12-4-4-4 4"/><path d="m18 12v6a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-6"/><path d="m2 12 4 4 4-4"/><path d="m6 12V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v6"/></svg>',
    'seoContent': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
    'security': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
    'privacy': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>',
    'compatibility': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"></rect><line x1="2" y1="10" x2="22" y2="10"></line></svg>',
    'marketing': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
    'conversion': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v10l-4-4"/><path d="m16 6-4 4"/><path d="M20.4 13.4A9 9 0 1 1 10.6 4.6"/></svg>',
    'accessibility': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>',
    'overall': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3 text-blue-400"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path><path d="m9 12 2 2 4-4"></path></svg>'
}

# Module descriptions
MODULE_DESCRIPTIONS = {
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

def get_module_icon(module_key: str) -> str:
    """Get the SVG icon for a module."""
    return MODULE_ICONS.get(module_key, MODULE_ICONS['overall'])

def get_module_description(module_key: str) -> str:
    """Get the description for a module."""
    return MODULE_DESCRIPTIONS.get(module_key, 'Module analysis and recommendations.')

def get_grade(score: int) -> str:
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

def get_rating_class(rating: str) -> str:
    """Convert rating to CSS class name."""
    return 'rating-' + rating.lower().replace(' ', '-')

def get_border_class(rating: str) -> str:
    """Convert rating to border CSS class name."""
    return 'border-' + rating.lower().replace(' ', '-')

def format_domain(url: str) -> str:
    """Extract and format domain from URL for filename."""
    import re
    # Remove protocol and www
    domain = re.sub(r'^https?://(www\.)?', '', url)
    # Remove trailing slash
    domain = domain.rstrip('/')
    # Replace dots with hyphens for filename
    return domain.replace('.', '-')

def validate_json_data(data: Dict[str, Any]) -> bool:
    """Validate that JSON data contains required fields."""
    required_fields = ['url', 'generatedAt', 'overallScore', 'overallRating']
    
    for field in required_fields:
        if field not in data:
            return False
    
    # Validate score is numeric
    try:
        score = int(data['overallScore'])
        if score < 0 or score > 100:
            return False
    except (ValueError, TypeError):
        return False
    
    return True

# PDF generation settings
PDF_SETTINGS = {
    'format': 'A4',
    'print_background': True,
    'prefer_css_page_size': True,
    'margin': {
        'top': '0.5in',
        'right': '0.5in',
        'bottom': '0.5in',
        'left': '0.5in'
    }
}

# File paths
DEFAULT_PATHS = {
    'watch_dir': 'reports-raw',
    'output_dir': 'reports-final',
    'template_dir': 'templates',
    'log_file': 'webevo_reports.log'
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file_handler': True,
    'console_handler': True
}
