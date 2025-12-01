"""Unit tests for score combination module."""
import unittest
from src.response_parser import URLSafetyResult
from src.score_combiner import (
    determine_final_verdict,
    generate_reasons,
    combine_scores
)


class TestDetermineFinalVerdict(unittest.TestCase):
    """Test verdict determination logic."""
    
    def test_api_dangerous(self):
        """Test API reports dangerous."""
        verdict = determine_final_verdict("dangerous", 10, True)
        self.assertEqual(verdict, "dangerous")
    
    def test_high_rule_score(self):
        """Test high rule score overrides safe API."""
        verdict = determine_final_verdict("safe", 70, True)
        self.assertEqual(verdict, "dangerous")
    
    def test_api_suspicious(self):
        """Test API reports suspicious."""
        verdict = determine_final_verdict("suspicious", 10, True)
        self.assertEqual(verdict, "suspicious")
    
    def test_safe_with_medium_score(self):
        """Test safe API with medium rule score."""
        verdict = determine_final_verdict("safe", 40, True)
        self.assertEqual(verdict, "suspicious")
    
    def test_safe_with_low_score(self):
        """Test safe API with low rule score."""
        verdict = determine_final_verdict("safe", 20, True)
        self.assertEqual(verdict, "safe")
    
    def test_api_unavailable_low_score(self):
        """Test API unavailable with low rule score."""
        verdict = determine_final_verdict(None, 20, False)
        self.assertEqual(verdict, "safe")
    
    def test_api_unavailable_medium_score(self):
        """Test API unavailable with medium rule score."""
        verdict = determine_final_verdict(None, 40, False)
        self.assertEqual(verdict, "suspicious")
    
    def test_api_unavailable_high_score(self):
        """Test API unavailable with high rule score."""
        verdict = determine_final_verdict(None, 70, False)
        self.assertEqual(verdict, "dangerous")


class TestGenerateReasons(unittest.TestCase):
    """Test reason generation."""
    
    def test_with_api_threats(self):
        """Test reasons with API threats."""
        api_result = URLSafetyResult(
            url="http://malware.test",
            status="dangerous",
            threat_types=["MALWARE", "PHISHING"]
        )
        rule_score = {
            "total_score": 50,
            "checks": {
                "url_length": {"score": 0, "reason": "Normal length"},
                "ip_address": {"score": 30, "reason": "Uses IP address"}
            }
        }
        reasons = generate_reasons(api_result, rule_score, True)
        self.assertGreater(len(reasons), 0)
        self.assertTrue(any("Google Safe Browsing" in r for r in reasons))
        self.assertTrue(any("IP address" in r for r in reasons))
    
    def test_with_safe_api(self):
        """Test reasons with safe API result."""
        api_result = URLSafetyResult(
            url="http://example.com",
            status="safe",
            threat_types=[]
        )
        rule_score = {
            "total_score": 0,
            "checks": {
                "url_length": {"score": 0, "reason": "Normal length"}
            }
        }
        reasons = generate_reasons(api_result, rule_score, True)
        self.assertTrue(any("no known threats" in r.lower() for r in reasons))
    
    def test_api_unavailable(self):
        """Test reasons when API is unavailable."""
        rule_score = {
            "total_score": 30,
            "checks": {
                "suspicious_keywords": {"score": 15, "reason": "Contains keywords"}
            }
        }
        reasons = generate_reasons(None, rule_score, False)
        self.assertTrue(any("unavailable" in r.lower() for r in reasons))


class TestCombineScores(unittest.TestCase):
    """Test score combination."""
    
    def test_combine_api_and_rules(self):
        """Test combining API result with rule score."""
        api_result = URLSafetyResult(
            url="http://test.com",
            status="safe",
            threat_types=[]
        )
        rule_score = {
            "total_score": 20,
            "checks": {}
        }
        
        result = combine_scores(api_result, rule_score, "http://test.com")
        
        self.assertEqual(result["url"], "http://test.com")
        self.assertIn("verdict", result)
        self.assertIn("api_data", result)
        self.assertIn("rule_based_score", result)
        self.assertIn("reasons", result)
        self.assertIn("timestamp", result)
        self.assertEqual(result["api_data"]["available"], True)
    
    def test_combine_with_api_unavailable(self):
        """Test combining when API is unavailable."""
        rule_score = {
            "total_score": 40,
            "checks": {}
        }
        
        result = combine_scores(None, rule_score, "http://test.com")
        
        self.assertEqual(result["api_data"]["available"], False)
        self.assertEqual(result["verdict"], "suspicious")


if __name__ == "__main__":
    unittest.main()
