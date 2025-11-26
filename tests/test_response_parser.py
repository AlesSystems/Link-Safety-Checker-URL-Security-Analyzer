"""Unit tests for response parser."""
import unittest
from datetime import datetime
from src.response_parser import parse_safe_browsing_response, URLSafetyResult


class TestResponseParser(unittest.TestCase):
    """Test cases for Safe Browsing API response parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_url = "http://malware.wicar.org/"
    
    def test_parse_safe_url_empty_response(self):
        """Test parsing empty response (safe URL)."""
        api_response = {}
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(result.url, self.test_url)
        self.assertEqual(result.status, "safe")
        self.assertEqual(result.threat_types, [])
        self.assertIsNotNone(result.timestamp)
    
    def test_parse_safe_url_no_matches(self):
        """Test parsing response with no matches (safe URL)."""
        api_response = {"matches": []}
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(result.status, "safe")
        self.assertEqual(result.threat_types, [])
    
    def test_parse_malware_threat(self):
        """Test parsing response with MALWARE threat."""
        api_response = {
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
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(result.status, "dangerous")
        self.assertIn("MALWARE", result.threat_types)
    
    def test_parse_social_engineering_threat(self):
        """Test parsing response with SOCIAL_ENGINEERING (phishing) threat."""
        api_response = {
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
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(result.status, "dangerous")
        self.assertIn("SOCIAL_ENGINEERING", result.threat_types)
    
    def test_parse_unwanted_software_threat(self):
        """Test parsing response with UNWANTED_SOFTWARE threat."""
        api_response = {
            "matches": [
                {
                    "threatType": "UNWANTED_SOFTWARE",
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": self.test_url},
                    "cacheDuration": "300s",
                    "threatEntryType": "URL"
                }
            ]
        }
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(result.status, "dangerous")
        self.assertIn("UNWANTED_SOFTWARE", result.threat_types)
    
    def test_parse_potentially_harmful_application(self):
        """Test parsing response with POTENTIALLY_HARMFUL_APPLICATION threat."""
        api_response = {
            "matches": [
                {
                    "threatType": "POTENTIALLY_HARMFUL_APPLICATION",
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": self.test_url},
                    "cacheDuration": "300s",
                    "threatEntryType": "URL"
                }
            ]
        }
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(result.status, "suspicious")
        self.assertIn("POTENTIALLY_HARMFUL_APPLICATION", result.threat_types)
    
    def test_parse_multiple_threats(self):
        """Test parsing response with multiple threat types."""
        api_response = {
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
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(result.status, "dangerous")
        self.assertIn("MALWARE", result.threat_types)
        self.assertIn("SOCIAL_ENGINEERING", result.threat_types)
        self.assertEqual(len(result.threat_types), 2)
    
    def test_parse_mixed_threats_dangerous_priority(self):
        """Test that dangerous threats take priority over suspicious."""
        api_response = {
            "matches": [
                {
                    "threatType": "POTENTIALLY_HARMFUL_APPLICATION",
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": self.test_url},
                    "cacheDuration": "300s",
                    "threatEntryType": "URL"
                },
                {
                    "threatType": "MALWARE",
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": self.test_url},
                    "cacheDuration": "300s",
                    "threatEntryType": "URL"
                }
            ]
        }
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(result.status, "dangerous")
    
    def test_parse_null_response(self):
        """Test parsing null/None response."""
        result = parse_safe_browsing_response(None, self.test_url)
        
        self.assertEqual(result.status, "safe")
        self.assertEqual(result.threat_types, [])
    
    def test_url_safety_result_to_dict(self):
        """Test URLSafetyResult to_dict conversion."""
        result = URLSafetyResult(
            url=self.test_url,
            status="dangerous",
            threat_types=["MALWARE"],
            raw_response={"matches": []}
        )
        
        result_dict = result.to_dict()
        
        self.assertEqual(result_dict["url"], self.test_url)
        self.assertEqual(result_dict["status"], "dangerous")
        self.assertIn("MALWARE", result_dict["threat_types"])
        self.assertIn("timestamp", result_dict)
        self.assertIn("raw_response", result_dict)
    
    def test_url_safety_result_repr(self):
        """Test URLSafetyResult string representation."""
        result = URLSafetyResult(
            url=self.test_url,
            status="safe",
            threat_types=[]
        )
        
        repr_str = repr(result)
        
        self.assertIn(self.test_url, repr_str)
        self.assertIn("safe", repr_str)
    
    def test_parse_malformed_response_missing_threat_type(self):
        """Test parsing response with missing threatType field."""
        api_response = {
            "matches": [
                {
                    "platformType": "ANY_PLATFORM",
                    "threat": {"url": self.test_url}
                }
            ]
        }
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(result.threat_types, [])
        self.assertEqual(result.status, "suspicious")
    
    def test_parse_duplicate_threat_types(self):
        """Test that duplicate threat types are not added multiple times."""
        api_response = {
            "matches": [
                {
                    "threatType": "MALWARE",
                    "platformType": "WINDOWS",
                    "threat": {"url": self.test_url}
                },
                {
                    "threatType": "MALWARE",
                    "platformType": "LINUX",
                    "threat": {"url": self.test_url}
                }
            ]
        }
        
        result = parse_safe_browsing_response(api_response, self.test_url)
        
        self.assertEqual(len(result.threat_types), 1)
        self.assertIn("MALWARE", result.threat_types)


if __name__ == '__main__':
    unittest.main()
