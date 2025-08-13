# WebEvo.ai Website Scanning & Report Generation System

An automated system that transforms raw website scan JSON data into professional PDF reports with WebEvo.ai branding. The system monitors a `reports-raw` directory for new scan files and automatically processes them to create branded reports.

## Features

- 🚀 **Automated Processing**: Monitors directory for new JSON files and processes them automatically
- 📊 **Professional Reports**: Generates high-quality PDF reports with WebEvo.ai branding
- 🎨 **Dynamic Templates**: Uses Jinja2 templates for flexible report customization
- 📱 **Full Content**: Generates reports with full height (no pagination)
- 🔄 **Real-time Monitoring**: File system event-driven processing
- 📝 **Comprehensive Logging**: Detailed logging for monitoring and debugging

## System Requirements

- Python 3.8 or higher
- macOS, Linux, or Windows
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd webevo-report-gen
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

```bash
playwright install chromium
```

### 4. Verify Installation

```bash
python webevo_report_generator.py --help
```

## Usage

### Basic Usage

#### Watch Directory for New Files (Default)

```bash
python webevo_report_generator.py
```

This will:
- Monitor the `reports-raw` directory for new JSON files
- Automatically generate PDF reports when files are detected
- Save reports to the `reports-final` directory

#### Process a Single File

```bash
python webevo_report_generator.py --single reports-raw/example.json
```

#### Custom Directories

```bash
python webevo_report_generator.py \
  --watch /path/to/input \
  --output /path/to/output \
  --template /path/to/templates
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--watch` | Directory to monitor for JSON files | `reports-raw` |
| `--output` | Directory to save generated reports | `reports-final` |
| `--template` | Directory containing HTML templates | `templates` |
| `--single` | Process a single JSON file instead of watching | None |

## Directory Structure

```
webevo-report-gen/
├── reports-raw/           # Input JSON files from website scans
├── reports-final/         # Generated PDF reports
├── templates/             # HTML templates for reports
│   └── report_template.html
├── webevo_report_generator.py  # Main script
├── config.py              # Configuration and helper functions
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── PRD.md               # Product Requirements Document
```

## JSON Data Format

The system expects JSON files with the following structure:

```json
{
  "url": "https://example.com/",
  "generatedAt": "2025-08-13T02:18:48.426Z",
  "overallScore": 75,
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
            "text": "Improve mobile responsiveness"
          }
        ]
      }
    }
  },
  "topRecommendations": {
    "items": [
      {
        "text": "Optimize page load speed"
      }
    ]
  }
}
```

### Required Fields

- `url`: The scanned website URL
- `generatedAt`: ISO timestamp of when the scan was performed
- `overallScore`: Numeric score (0-100)
- `overallRating`: Text rating (e.g., "Poor", "Good", "Excellent")

### Optional Fields

- `modules`: Individual module scores and recommendations
- `topRecommendations`: Priority recommendations list
- `reportId`: Unique identifier for the report
- `schemaVersion`: Version of the data schema

## Report Output

### File Naming Convention

Reports are named using the pattern:
```
{domain}_{date}_{webevo-ai}.pdf
```

Example: `eastmountaindental-com_2025-08-13_webevo-ai.pdf`

### Report Content

Each generated report includes:

- **Header**: WebEvo.ai branding and website URL
- **Overall Score**: Visual score representation with grade
- **Module Scores**: Individual category scores and ratings
- **Recommendations**: Detailed action items for improvement
- **Footer**: Generation timestamp and branding

## Configuration

### Customizing Templates

Edit `templates/report_template.html` to modify the report appearance:

- Change colors and styling
- Add new sections
- Modify layout and branding

### Module Icons and Descriptions

Update `config.py` to customize:

- Module-specific icons (SVG)
- Module descriptions
- Rating color schemes
- PDF generation settings

## Monitoring and Logging

### Log Files

The system creates detailed logs in `webevo_reports.log`:

```
2025-08-13 10:30:15 - INFO - Started watching directory: reports-raw
2025-08-13 10:30:20 - INFO - Processing new file: reports-raw/example.json
2025-08-13 10:30:25 - INFO - Successfully generated report: reports-final/example_2025-08-13_webevo-ai.pdf
```

### Error Handling

The system includes comprehensive error handling:

- Invalid JSON files are logged and skipped
- PDF generation failures are logged with details
- File system errors are handled gracefully

## Troubleshooting

### Common Issues

#### Playwright Installation Problems

```bash
# Reinstall Playwright
pip uninstall playwright
pip install playwright
playwright install chromium
```

#### Template Loading Errors

Ensure the template directory exists:
```bash
mkdir -p templates
# Copy the default template
cp templates/report_template.html templates/
```

#### Permission Errors

Check directory permissions:
```bash
chmod 755 reports-raw reports-final
```

#### Memory Issues

For large reports, increase system memory or optimize the template.

### Debug Mode

Enable verbose logging:

```python
# In webevo_report_generator.py
logging.basicConfig(level=logging.DEBUG)
```

## Development

### Adding New Modules

1. Update `config.py` with new module icons and descriptions
2. Modify the HTML template to include new module sections
3. Update the JSON parsing logic if needed

### Customizing Report Styles

1. Edit the CSS in `templates/report_template.html`
2. Modify the Tailwind CSS classes
3. Add custom JavaScript for interactive elements

### Testing

```bash
# Test with sample data
python webevo_report_generator.py --single test-data.json

# Test file watching
python webevo_report_generator.py --watch test-input --output test-output
```

## Performance

### Optimization Tips

- Use efficient HTML templates
- Minimize external dependencies
- Implement caching for repeated data
- Monitor memory usage for large reports

### Benchmarks

- **Processing Time**: < 30 seconds per report
- **Memory Usage**: < 500MB per report
- **Concurrent Processing**: Supports multiple simultaneous reports

## Security Considerations

- Input validation for JSON data
- HTML content sanitization
- Secure file handling
- No sensitive data in logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is proprietary to WebEvo.ai. All rights reserved.

## Support

For technical support or questions:

- Check the logs for error details
- Review the troubleshooting section
- Contact the development team

## Roadmap

### Future Enhancements

- [ ] Email integration for automatic report delivery
- [ ] Multiple report template styles
- [ ] Batch processing capabilities
- [ ] RESTful API endpoints
- [ ] Cloud deployment options
- [ ] Advanced analytics and reporting

### Version History

- **v1.0.0**: Initial release with basic functionality
- **v1.1.0**: Enhanced error handling and logging
- **v1.2.0**: Template customization and configuration options

---

**WebEvo.ai** - Transforming website analysis into actionable insights.
