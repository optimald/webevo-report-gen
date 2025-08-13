#!/bin/bash

# WebEvo.ai Report Generator - Installation Script
# This script installs the required dependencies and sets up the system

set -e

echo "🚀 WebEvo.ai Report Generator - Installation Script"
echo "=================================================="

# Check if Python 3.8+ is installed
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION found"

# Check if pip is installed
echo "🔍 Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi
echo "✅ pip3 found"

# Create virtual environment (optional)
read -p "🤔 Would you like to create a virtual environment? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment created and activated"
    echo "💡 To activate in the future, run: source venv/bin/activate"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✅ Python dependencies installed"

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium
echo "✅ Playwright browsers installed"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p reports-raw reports-final templates
echo "✅ Directories created"

# Set permissions
echo "🔐 Setting file permissions..."
chmod +x webevo_report_generator.py
chmod +x test_report_generation.py
echo "✅ Permissions set"

# Test installation
echo "🧪 Testing installation..."
if python3 test_report_generation.py; then
    echo "✅ Installation test passed!"
else
    echo "⚠️  Installation test had issues, but installation may still work"
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Add JSON scan files to the 'reports-raw' directory"
echo "2. Run: python3 webevo_report_generator.py"
echo "3. Check 'reports-final' for generated PDF reports"
echo ""
echo "📚 For more information, see README.md"
echo "🐛 For issues, check the logs or run the test script"
echo ""
echo "Happy reporting! 🚀"
