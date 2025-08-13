#!/usr/bin/env python3
"""
Setup script for WebEvo.ai Report Generator
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="webevo-report-generator",
    version="1.0.0",
    author="WebEvo.ai",
    author_email="team@webevo.ai",
    description="Automated website scan report generation system with WebEvo.ai branding",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/webevo-ai/webevo-report-gen",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "webevo-report-gen=webevo_report_generator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*.html", "*.md", "*.txt"],
    },
    keywords="website, scanning, reports, pdf, automation, webevo",
    project_urls={
        "Bug Reports": "https://github.com/webevo-ai/webevo-report-gen/issues",
        "Source": "https://github.com/webevo-ai/webevo-report-gen",
        "Documentation": "https://github.com/webevo-ai/webevo-report-gen#readme",
    },
)
