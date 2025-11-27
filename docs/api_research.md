# API Research and Implementation

## API Selection: Google Safe Browsing API (v4)

We have selected **Google Safe Browsing API (v4)** for this project. For detailed research on all considered options, see the Ticket.md file.

### Key Features
- Industry-standard service used by major browsers (Chrome, Safari, Firefox)
- Detects Malware, Social Engineering (Phishing), Unwanted Software, and Potentially Harmful Applications
- Generous free tier (~10,000 requests/day)
- Synchronous response for immediate results

### Requirements
1. **GCP Project**: Create a project in Google Cloud Console
2. **API Key**: Generate an API key restricted to "Safe Browsing API"
3. **Library**: Python `requests` module
4. **Endpoint**: `https://safebrowsing.googleapis.com/v4/threatMatches:find`

### Rate Limits
- **Free Tier**: ~10,000 requests per day
- **QPS**: Queries per second limits apply but are sufficient for typical usage

## Implementation Details

### Configuration (`src/config.py`)
- Manages API key loading from environment variables
- Stores API endpoint and request parameters
- Configures threat types to check: MALWARE, SOCIAL_ENGINEERING, UNWANTED_SOFTWARE, POTENTIALLY_HARMFUL_APPLICATION

### API Client (`src/api_client.py`)
- `check_url_safety(url)`: Main function to check URL safety
- Returns parsed JSON response from API
- **Error Handling**:
  - `APIKeyError`: Invalid or missing API key (HTTP 400/403)
  - `RateLimitError`: Rate limit exceeded (HTTP 429)
  - `NetworkError`: Timeout or connection failures
  - `SafeBrowsingAPIError`: General API errors

### Response Parser (`src/response_parser.py`)
- `parse_safe_browsing_response(api_response, url)`: Converts API response to simplified classification
- **Classification Mapping**:
  - **safe**: Empty response or no threat matches
  - **dangerous**: MALWARE, UNWANTED_SOFTWARE, SOCIAL_ENGINEERING detected
  - **suspicious**: POTENTIALLY_HARMFUL_APPLICATION detected
- Returns `URLSafetyResult` object with status, threat types, and timestamp

### Testing
- Comprehensive unit tests with mocked API responses
- Tests for all success scenarios (safe, dangerous, suspicious URLs)
- Tests for all error scenarios (timeout, rate limit, invalid key, network errors)
- Uses `unittest.mock` to avoid real API calls during testing

## Usage Example

```python
from src.api_client import check_url_safety
from src.response_parser import parse_safe_browsing_response

# Check a URL
url = "https://example.com"
api_response = check_url_safety(url)

# Parse the response
result = parse_safe_browsing_response(api_response, url)

print(f"URL: {result.url}")
print(f"Status: {result.status}")
print(f"Threats: {result.threat_types}")
print(f"Checked at: {result.timestamp}")
```

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Add your Google Safe Browsing API key to `.env`:
   ```
   GOOGLE_SAFE_BROWSING_API_KEY=your_actual_api_key_here
   ```

4. Run tests:
   ```bash
   python -m pytest tests/ -v
   ```
