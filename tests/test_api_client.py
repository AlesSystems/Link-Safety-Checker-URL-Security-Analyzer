"""Unit tests for API client with mocked responses."""
import unittest
from unittest.mock import patch, Mock
import requests
from src.api_client import (
    check_url_safety,
    SafeBrowsingAPIError,
    APIKeyError,
    RateLimitError,
    NetworkError
)


class TestSafeBrowsingAPIClient(unittest.TestCase):
    """Test cases for Safe Browsing API client."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_url = "https://example.com"
        self.api_key = "test_api_key_12345"
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_successful_request_with_no_threats(self, mock_post):
        """Test successful API request with no threats detected (safe URL)."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_post.return_value = mock_response
        
        result = check_url_safety(self.test_url)
        
        self.assertEqual(result, {})
        mock_post.assert_called_once()
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_successful_request_with_malware_threat(self, mock_post):
        """Test successful API request with MALWARE threat detected."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "matches": [
                {
                    "threatType": "MALWARE",
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": self.test_url},
                    "cacheDuration": "300s",
                    "threatEntryType": "URL"
                }
            ]
        }
        mock_post.return_value = mock_response
        
        result = check_url_safety(self.test_url)
        
        self.assertIn("matches", result)
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["matches"][0]["threatType"], "MALWARE")
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_successful_request_with_phishing_threat(self, mock_post):
        """Test successful API request with SOCIAL_ENGINEERING (phishing) threat."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "matches": [
                {
                    "threatType": "SOCIAL_ENGINEERING",
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": self.test_url},
                    "cacheDuration": "300s",
                    "threatEntryType": "URL"
                }
            ]
        }
        mock_post.return_value = mock_response
        
        result = check_url_safety(self.test_url)
        
        self.assertIn("matches", result)
        self.assertEqual(result["matches"][0]["threatType"], "SOCIAL_ENGINEERING")
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_successful_request_with_multiple_threats(self, mock_post):
        """Test successful API request with multiple threat types."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "matches": [
                {
                    "threatType": "MALWARE",
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": self.test_url},
                    "cacheDuration": "300s",
                    "threatEntryType": "URL"
                },
                {
                    "threatType": "SOCIAL_ENGINEERING",
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": self.test_url},
                    "cacheDuration": "300s",
                    "threatEntryType": "URL"
                }
            ]
        }
        mock_post.return_value = mock_response
        
        result = check_url_safety(self.test_url)
        
        self.assertEqual(len(result["matches"]), 2)
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', None)
    def test_missing_api_key(self):
        """Test error handling when API key is missing."""
        with self.assertRaises(APIKeyError) as context:
            check_url_safety(self.test_url)
        
        self.assertIn("not configured", str(context.exception))
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_invalid_api_key_400_error(self, mock_post):
        """Test error handling for HTTP 400 (invalid API key)."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Invalid API key"
        mock_post.return_value = mock_response
        
        with self.assertRaises(APIKeyError) as context:
            check_url_safety(self.test_url)
        
        self.assertIn("Invalid API key", str(context.exception))
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_forbidden_403_error(self, mock_post):
        """Test error handling for HTTP 403 (forbidden/API key restrictions)."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "API key restrictions"
        mock_post.return_value = mock_response
        
        with self.assertRaises(APIKeyError) as context:
            check_url_safety(self.test_url)
        
        self.assertIn("restrictions", str(context.exception))
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_rate_limit_429_error(self, mock_post):
        """Test error handling for HTTP 429 (rate limit exceeded)."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "60"}
        mock_response.text = "Rate limit exceeded"
        mock_post.return_value = mock_response
        
        with self.assertRaises(RateLimitError) as context:
            check_url_safety(self.test_url)
        
        self.assertIn("Rate limit exceeded", str(context.exception))
        self.assertIn("60", str(context.exception))
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_timeout_error(self, mock_post):
        """Test error handling for request timeout."""
        mock_post.side_effect = requests.exceptions.Timeout()
        
        with self.assertRaises(NetworkError) as context:
            check_url_safety(self.test_url)
        
        self.assertIn("timeout", str(context.exception).lower())
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_connection_error(self, mock_post):
        """Test error handling for network connection error."""
        mock_post.side_effect = requests.exceptions.ConnectionError("Failed to connect")
        
        with self.assertRaises(NetworkError) as context:
            check_url_safety(self.test_url)
        
        self.assertIn("Failed to connect", str(context.exception))
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_json_parsing_error(self, mock_post):
        """Test error handling for malformed JSON response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response
        
        with self.assertRaises(SafeBrowsingAPIError) as context:
            check_url_safety(self.test_url)
        
        self.assertIn("parse", str(context.exception).lower())
    
    @patch('src.api_client.GOOGLE_SAFE_BROWSING_API_KEY', 'test_api_key')
    @patch('src.api_client.requests.post')
    def test_unexpected_status_code(self, mock_post):
        """Test error handling for unexpected HTTP status codes."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_post.return_value = mock_response
        
        with self.assertRaises(SafeBrowsingAPIError) as context:
            check_url_safety(self.test_url)
        
        self.assertIn("500", str(context.exception))


if __name__ == '__main__':
    unittest.main()
