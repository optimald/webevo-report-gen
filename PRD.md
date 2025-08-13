# WebEvo.ai Website Scanning & Report Generation System - PRD

## 1. Executive Summary

The WebEvo.ai Website Scanning & Report Generation System is an automated solution that processes website scan results from JSON files and generates professional PDF reports with WebEvo.ai branding. The system monitors a `reports-raw` directory for new scan files and automatically processes them to create branded reports in the `reports-final` directory.

## 2. Product Overview

### 2.1 Purpose
Transform raw website scan JSON data into professional, branded PDF reports that can be shared with clients, stakeholders, or used for internal analysis.

### 2.2 Target Users
- WebEvo.ai team members
- Website developers and agencies
- Business stakeholders requiring website analysis reports
- Compliance and audit teams

### 2.3 Key Benefits
- Automated report generation
- Consistent branding and formatting
- Professional presentation of technical data
- Time-saving automation
- Standardized report format

## 3. Functional Requirements

### 3.1 Core Functionality

#### 3.1.1 File Monitoring
- **Requirement**: Monitor `reports-raw` directory for new JSON files
- **Trigger**: File system events (file creation/modification)
- **Action**: Automatically start processing when new files are detected

#### 3.1.2 JSON Data Processing
- **Input**: JSON files from website scanning tool
- **Processing**: Parse and extract key metrics and recommendations
- **Output**: Structured data for HTML template population

#### 3.1.3 HTML Template Population
- **Template**: Use existing `aisav.com.html` as base template
- **Data Mapping**: Populate template with scan results
- **Dynamic Content**: Generate scores, ratings, recommendations, and visual elements

#### 3.1.4 Report Generation
- **Format**: PDF (preferred) or PNG fallback
- **Dimensions**: Full height of content (no pagination)
- **Quality**: High-resolution, professional appearance

### 3.2 Data Requirements

#### 3.2.1 Required JSON Fields
- `url`: Scanned website URL
- `generatedAt`: Scan timestamp
- `overallScore`: Overall website score
- `overallRating`: Overall rating (e.g., "Poor", "Good")
- `modules`: Individual module scores and recommendations
- `topRecommendations`: Priority recommendations list

#### 3.2.2 Optional Fields
- `reportId`: Unique report identifier
- `schemaVersion`: Data schema version
- `industryContext`: Industry-specific analysis
- `viewports`: Device-specific analysis results

### 3.3 Output Requirements

#### 3.3.1 File Naming Convention
```
{scanned-site-url}_{scan-date}_{webevo-ai}.pdf
```
Example: `eastmountaindental-com_2025-08-13_webevo-ai.pdf`

#### 3.3.2 File Organization
- **Source**: `reports-raw/` - Raw JSON scan files
- **Output**: `reports-final/` - Generated PDF reports
- **Templates**: `templates/` - HTML template files

## 4. Technical Requirements

### 4.1 Technology Stack

#### 4.1.1 Core Technologies
- **Language**: Python 3.8+
- **Web Automation**: Playwright
- **PDF Generation**: Playwright PDF capabilities
- **File Monitoring**: Watchdog library
- **HTML Processing**: BeautifulSoup4 or similar

#### 4.1.2 Dependencies
- `playwright`: Web automation and PDF generation
- `watchdog`: File system monitoring
- `jinja2`: HTML template rendering
- `click`: Command-line interface

### 4.2 System Architecture

#### 4.2.1 Components
1. **File Monitor**: Watches for new JSON files
2. **Data Processor**: Parses and validates JSON data
3. **Template Engine**: Renders HTML with scan data
4. **PDF Generator**: Converts HTML to PDF
5. **File Manager**: Organizes input/output files

#### 4.2.2 Data Flow
```
JSON File → Data Parser → Template Engine → HTML → PDF Generator → Final Report
```

### 4.3 Performance Requirements
- **Processing Time**: < 30 seconds per report
- **Memory Usage**: < 500MB per report
- **Concurrent Processing**: Support for multiple simultaneous reports
- **Error Handling**: Graceful failure with detailed logging

## 5. User Experience Requirements

### 5.1 Report Design
- **Branding**: Prominent WebEvo.ai logo and branding
- **Layout**: Professional, clean design with clear hierarchy
- **Colors**: Consistent with WebEvo.ai brand guidelines
- **Typography**: Readable fonts with proper contrast

### 5.2 Content Organization
- **Header**: Website URL, scan date, WebEvo.ai branding
- **Summary**: Overall score with visual representation
- **Modules**: Individual category scores and ratings
- **Recommendations**: Prioritized action items
- **Footer**: Generation timestamp and branding

### 5.3 Visual Elements
- **Score Rings**: Circular progress indicators for scores
- **Color Coding**: Consistent rating color scheme
- **Icons**: Module-specific visual indicators
- **Charts**: Visual representation of performance metrics

## 6. Non-Functional Requirements

### 6.1 Reliability
- **Uptime**: 99.9% availability during business hours
- **Error Recovery**: Automatic retry for failed generations
- **Data Integrity**: Preserve original JSON data
- **Backup**: Archive of generated reports

### 6.2 Security
- **File Access**: Secure handling of scan data
- **Output Validation**: Sanitize HTML content
- **Error Logging**: No sensitive data in logs

### 6.3 Scalability
- **Volume**: Handle 100+ reports per day
- **Storage**: Efficient file management and cleanup
- **Performance**: Linear scaling with increased load

## 7. Implementation Phases

### 7.1 Phase 1: Core System (Week 1-2)
- Basic file monitoring setup
- JSON parsing and validation
- HTML template population
- PDF generation with Playwright

### 7.2 Phase 2: Automation & Monitoring (Week 3)
- File system event handling
- Error handling and logging
- Command-line interface
- Basic testing and validation

### 7.3 Phase 3: Enhancement & Polish (Week 4)
- Advanced error handling
- Performance optimization
- Documentation and deployment
- User acceptance testing

## 8. Success Metrics

### 8.1 Technical Metrics
- **Processing Success Rate**: > 95%
- **Average Generation Time**: < 30 seconds
- **Error Rate**: < 2%
- **System Uptime**: > 99%

### 8.2 Business Metrics
- **Report Quality**: Professional appearance and accuracy
- **User Satisfaction**: Positive feedback on report format
- **Time Savings**: Reduced manual report creation time
- **Brand Consistency**: Consistent WebEvo.ai presentation

## 9. Risk Assessment

### 9.1 Technical Risks
- **Playwright Compatibility**: Browser automation issues
- **PDF Generation**: Quality and formatting problems
- **File System Events**: Missed file detection
- **Memory Usage**: Large report processing issues

### 9.2 Mitigation Strategies
- **Testing**: Comprehensive testing across environments
- **Fallbacks**: PNG generation as backup option
- **Monitoring**: Robust error logging and alerting
- **Resource Management**: Memory and CPU usage limits

## 10. Future Enhancements

### 10.1 Advanced Features
- **Email Integration**: Automatic report delivery
- **Custom Templates**: Multiple report styles
- **Batch Processing**: Bulk report generation
- **API Integration**: RESTful endpoints for automation

### 10.2 Analytics & Reporting
- **Usage Metrics**: System performance tracking
- **Report Analytics**: Popular content and formats
- **Performance Monitoring**: System health dashboards

## 11. Conclusion

The WebEvo.ai Website Scanning & Report Generation System will provide an automated, professional solution for transforming raw scan data into branded reports. The system's focus on automation, quality, and brand consistency will significantly improve the efficiency of report generation while maintaining the professional standards expected by WebEvo.ai clients.

The implementation will be developed locally with the option for future cloud deployment, ensuring immediate value while maintaining flexibility for future growth.
