Technical Requirements
# Required packages from requirements.txt
streamlit      # Web application framework
beautifulsoup4 # HTML parsing
lxml          # XML/HTML processor

URL Structure
Base URL: https://www.amazon.in
Product URLs are automatically constructed by appending product-specific paths
Example: https://www.amazon.in/[product-specific-path]


Email Configuration
SMTP Server: smtp.gmail.com
Port: 465
Security: SSL
Required Credentials:
Gmail address
App-specific password

usage

1) Run the application using command:
streamlit run amazon_tracker.py

2) Input required information:
Price threshold
Upload Amazon HTML file
Email credentials (optional)
Recipient email (optional)

Data Flow
HTML File Upload → BeautifulSoup Parsing
Product Information Extraction
Price Comparison
Display Results
Email Alert (if configured)
