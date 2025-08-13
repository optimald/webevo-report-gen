# WebEvo.ai Report Generator - Makefile
# Common commands for development and deployment

.PHONY: help install test demo clean run watch setup

# Default target
help:
	@echo "🚀 WebEvo.ai Report Generator - Available Commands"
	@echo "=================================================="
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  make install     - Install Python dependencies and Playwright"
	@echo "  make setup       - Create necessary directories and set permissions"
	@echo ""
	@echo "🧪 Testing & Development:"
	@echo "  make test        - Run the test suite"
	@echo "  make demo        - Run the demo script"
	@echo ""
	@echo "🚀 Running the System:"
	@echo "  make run         - Process a single existing JSON file"
	@echo "  make watch       - Start watching for new JSON files"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  make clean       - Clean up generated files and logs"
	@echo "  make logs        - View recent logs"
	@echo ""
	@echo "📚 Documentation:"
	@echo "  make help        - Show this help message"

# Install dependencies
install:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "🌐 Installing Playwright browsers..."
	playwright install chromium
	@echo "✅ Installation complete!"

# Setup directories and permissions
setup:
	@echo "📁 Creating necessary directories..."
	mkdir -p reports-raw reports-final templates
	@echo "🔐 Setting file permissions..."
	chmod +x webevo_report_generator.py
	chmod +x test_report_generation.py
	chmod +x demo.py
	@echo "✅ Setup complete!"

# Run tests
test:
	@echo "🧪 Running test suite..."
	python test_report_generation.py

# Run demo
demo:
	@echo "🎭 Running demo..."
	python demo.py

# Process existing file
run:
	@echo "📄 Processing existing JSON file..."
	@if [ -f "reports-raw/2025-08-13_02-19-34-900Z_eastmountaindental-com_6323faea.json" ]; then \
		python webevo_report_generator.py --single "reports-raw/2025-08-13_02-19-34-900Z_eastmountaindental-com_6323faea.json"; \
	else \
		echo "❌ No existing JSON file found. Add files to reports-raw/ directory first."; \
	fi

# Start watching for new files
watch:
	@echo "👀 Starting file watcher..."
	python webevo_report_generator.py

# Clean up generated files
clean:
	@echo "🧹 Cleaning up generated files..."
	rm -f reports-final/*.pdf
	rm -f *.log
	rm -f demo-data.json
	@echo "✅ Cleanup complete!"

# View recent logs
logs:
	@echo "📝 Recent logs:"
	@if [ -f "webevo_reports.log" ]; then \
		tail -20 webevo_reports.log; \
	else \
		echo "No log file found."; \
	fi

# Full installation (install + setup)
all: install setup

# Quick start (setup + demo)
quick: setup demo

# Development mode (setup + test + demo)
dev: setup test demo
