"""Unit tests for risk scoring module."""
import unittest
from src.risk_scorer import (
    analyze_url_length,
    check_ip_address,
    detect_suspicious_keywords,
    check_tld,
    check_port,
    calculate_rule_score
)


class TestURLLengthAnalysis(unittest.TestCase):
    """Test URL length analysis."""
    
    def test_normal_length(self):
        """Test normal length URL."""
        url = "https://example.com/page"
        result = analyze_url_length(url)
        self.assertEqual(result["score"], 0)
        self.assertIn("normal", result["reason"].lower())
    
    def test_suspicious_length(self):
        """Test suspicious length URL (201-500 chars)."""
        url = "https://example.com/" + "a" * 300
        result = analyze_url_length(url)
        self.assertEqual(result["score"], 20)
        self.assertIn("suspicious", result["reason"].lower())
    
    def test_dangerous_length(self):
        """Test extremely long URL (>500 chars)."""
        url = "https://example.com/" + "a" * 600
        result = analyze_url_length(url)
        self.assertEqual(result["score"], 40)
        self.assertIn("extremely long", result["reason"].lower())


class TestIPAddressCheck(unittest.TestCase):
    """Test IP address detection."""
    
    def test_domain_name(self):
        """Test URL with domain name."""
        url = "https://google.com/search"
        result = check_ip_address(url)
        self.assertEqual(result["score"], 0)
        self.assertIn("domain", result["reason"].lower())
    
    def test_ipv4_address(self):
        """Test URL with IPv4 address."""
        url = "http://192.168.1.1/page"
        result = check_ip_address(url)
        self.assertEqual(result["score"], 30)
        self.assertIn("IP address", result["reason"])
    
    def test_ipv6_address(self):
        """Test URL with IPv6 address."""
        url = "http://[2001:db8::1]/page"
        result = check_ip_address(url)
        self.assertEqual(result["score"], 30)


class TestSuspiciousKeywords(unittest.TestCase):
    """Test suspicious keyword detection."""
    
    def test_no_keywords(self):
        """Test URL with no suspicious keywords."""
        url = "https://example.com/about"
        result = detect_suspicious_keywords(url)
        self.assertEqual(result["score"], 0)
        self.assertIn("No suspicious", result["reason"])
    
    def test_one_keyword(self):
        """Test URL with one suspicious keyword."""
        url = "https://example.com/login"
        result = detect_suspicious_keywords(url)
        self.assertEqual(result["score"], 15)
        self.assertIn("login", result["reason"].lower())
    
    def test_multiple_keywords(self):
        """Test URL with multiple suspicious keywords."""
        url = "https://example.com/secure-login-verify-account"
        result = detect_suspicious_keywords(url)
        self.assertEqual(result["score"], 30)
        self.assertIn("multiple", result["reason"].lower())


class TestTLDCheck(unittest.TestCase):
    """Test TLD checking."""
    
    def test_standard_tld(self):
        """Test URL with standard TLD."""
        url = "https://example.com/page"
        result = check_tld(url)
        self.assertEqual(result["score"], 0)
        self.assertIn("standard", result["reason"].lower())
    
    def test_suspicious_tld(self):
        """Test URL with suspicious TLD."""
        url = "https://example.tk/page"
        result = check_tld(url)
        self.assertEqual(result["score"], 25)
        self.assertIn("suspicious TLD", result["reason"])


class TestPortCheck(unittest.TestCase):
    """Test port checking."""
    
    def test_no_port(self):
        """Test URL without explicit port."""
        url = "https://example.com/page"
        result = check_port(url)
        self.assertEqual(result["score"], 0)
        self.assertIn("default", result["reason"].lower())
    
    def test_standard_port(self):
        """Test URL with standard port."""
        url = "http://example.com:80/page"
        result = check_port(url)
        self.assertEqual(result["score"], 0)
        self.assertIn("standard", result["reason"].lower())
    
    def test_uncommon_port(self):
        """Test URL with uncommon port."""
        url = "http://example.com:8888/page"
        result = check_port(url)
        self.assertEqual(result["score"], 20)
        self.assertIn("uncommon", result["reason"].lower())


class TestCalculateRuleScore(unittest.TestCase):
    """Test comprehensive rule scoring."""
    
    def test_safe_url(self):
        """Test safe URL with low score."""
        url = "https://google.com"
        result = calculate_rule_score(url)
        self.assertIn("total_score", result)
        self.assertIn("checks", result)
        self.assertEqual(len(result["checks"]), 5)
        self.assertLess(result["total_score"], 30)
    
    def test_suspicious_url(self):
        """Test suspicious URL with medium score."""
        url = "http://192.168.1.1:8888/secure-login-verify"
        result = calculate_rule_score(url)
        self.assertGreater(result["total_score"], 30)
    
    def test_dangerous_url(self):
        """Test dangerous URL with high score."""
        long_path = "a" * 600
        url = f"http://192.168.1.1:9999/secure-login-bank-verify-account-{long_path}"
        result = calculate_rule_score(url)
        self.assertGreater(result["total_score"], 60)


if __name__ == "__main__":
    unittest.main()
