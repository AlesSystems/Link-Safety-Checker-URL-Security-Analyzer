"""Unit tests for verdict module."""
import unittest
import json
from src.verdict import FinalSecurityVerdict


class TestFinalSecurityVerdict(unittest.TestCase):
    """Test FinalSecurityVerdict class."""
    
    def setUp(self):
        """Set up test data."""
        self.verdict_data = {
            "url": "http://test.com",
            "verdict": "suspicious",
            "api_data": {
                "status": "safe",
                "threat_types": [],
                "available": True
            },
            "rule_based_score": {
                "total_score": 45,
                "checks": {
                    "url_length": {"score": 0, "reason": "Normal"},
                    "ip_address": {"score": 30, "reason": "Uses IP"},
                    "suspicious_keywords": {"score": 15, "reason": "Keywords"}
                }
            },
            "reasons": ["Google Safe Browsing reports no threats", "Uses IP address"],
            "timestamp": "2023-01-01T00:00:00Z"
        }
    
    def test_initialization(self):
        """Test verdict initialization."""
        verdict = FinalSecurityVerdict(**self.verdict_data)
        self.assertEqual(verdict.url, "http://test.com")
        self.assertEqual(verdict.verdict, "suspicious")
        self.assertTrue(verdict.api_data["available"])
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        verdict = FinalSecurityVerdict(**self.verdict_data)
        result = verdict.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["url"], "http://test.com")
        self.assertEqual(result["verdict"], "suspicious")
        self.assertIn("api_data", result)
        self.assertIn("rule_based_score", result)
        self.assertIn("reasons", result)
        self.assertIn("timestamp", result)
    
    def test_to_json(self):
        """Test conversion to JSON."""
        verdict = FinalSecurityVerdict(**self.verdict_data)
        json_str = verdict.to_json()
        
        self.assertIsInstance(json_str, str)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["url"], "http://test.com")
    
    def test_is_safe(self):
        """Test is_safe method."""
        safe_verdict = FinalSecurityVerdict(
            url="http://safe.com",
            verdict="safe",
            api_data={},
            rule_based_score={},
            reasons=[]
        )
        self.assertTrue(safe_verdict.is_safe())
        self.assertFalse(safe_verdict.is_suspicious())
        self.assertFalse(safe_verdict.is_dangerous())
    
    def test_is_suspicious(self):
        """Test is_suspicious method."""
        verdict = FinalSecurityVerdict(**self.verdict_data)
        self.assertTrue(verdict.is_suspicious())
        self.assertFalse(verdict.is_safe())
        self.assertFalse(verdict.is_dangerous())
    
    def test_is_dangerous(self):
        """Test is_dangerous method."""
        dangerous_verdict = FinalSecurityVerdict(
            url="http://danger.com",
            verdict="dangerous",
            api_data={},
            rule_based_score={},
            reasons=[]
        )
        self.assertTrue(dangerous_verdict.is_dangerous())
        self.assertFalse(dangerous_verdict.is_safe())
        self.assertFalse(dangerous_verdict.is_suspicious())
    
    def test_get_summary(self):
        """Test summary generation."""
        verdict = FinalSecurityVerdict(**self.verdict_data)
        summary = verdict.get_summary()
        
        self.assertIsInstance(summary, str)
        self.assertIn("SUSPICIOUS", summary)
        self.assertIn("45", summary)
        self.assertIn("available", summary.lower())
    
    def test_timestamp_auto_generation(self):
        """Test automatic timestamp generation."""
        verdict = FinalSecurityVerdict(
            url="http://test.com",
            verdict="safe",
            api_data={},
            rule_based_score={},
            reasons=[]
        )
        self.assertIsNotNone(verdict.timestamp)
        self.assertIn("T", verdict.timestamp)


if __name__ == "__main__":
    unittest.main()
