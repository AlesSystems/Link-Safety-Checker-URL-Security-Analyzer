"""Rule-based risk scoring for URLs."""
import re
import ipaddress
from typing import Dict, Any, List
from urllib.parse import urlparse


SUSPICIOUS_KEYWORDS = [
    'secure', 'verify', 'update', 'account', 'login', 'signin', 'bank',
    'paypal', 'confirm', 'password', 'billing', 'credit', 'card', 'security',
    'suspended', 'verify', 'authenticate', 'wallet', 'tax', 'refund'
]

SUSPICIOUS_TLDS = [
    '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click',
    '.link', '.country', '.stream', '.download', '.win', '.bid', '.racing'
]


def analyze_url_length(url: str) -> Dict[str, Any]:
    """
    Analyze URL length for suspicious patterns.
    
    Scoring:
    - 0-200 chars: 0 points (normal)
    - 201-500 chars: 20 points (suspicious)
    - 501+ chars: 40 points (very suspicious)
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dict with score and reason
    """
    length = len(url)
    
    if length <= 200:
        return {
            "score": 0,
            "reason": f"URL length is normal ({length} characters)"
        }
    elif length <= 500:
        return {
            "score": 20,
            "reason": f"URL is suspiciously long ({length} characters)"
        }
    else:
        return {
            "score": 40,
            "reason": f"URL is extremely long ({length} characters), typical of obfuscated phishing URLs"
        }


def check_ip_address(url: str) -> Dict[str, Any]:
    """
    Check if URL uses IP address instead of domain name.
    
    Scoring:
    - Domain name: 0 points (normal)
    - IP address: 30 points (suspicious)
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dict with score and reason
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or parsed.netloc.split(':')[0]
        
        if not hostname:
            return {
                "score": 0,
                "reason": "Could not determine hostname"
            }
        
        try:
            ipaddress.ip_address(hostname)
            return {
                "score": 30,
                "reason": f"URL uses IP address ({hostname}) instead of domain name"
            }
        except ValueError:
            return {
                "score": 0,
                "reason": "URL uses domain name (normal)"
            }
    except Exception:
        return {
            "score": 0,
            "reason": "Could not parse URL"
        }


def detect_suspicious_keywords(url: str) -> Dict[str, Any]:
    """
    Detect phishing-related keywords in URL.
    
    Scoring:
    - No keywords: 0 points
    - 1-2 keywords: 15 points
    - 3+ keywords: 30 points
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dict with score, reason, and detected keywords
    """
    url_lower = url.lower()
    found_keywords = []
    
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url_lower:
            found_keywords.append(keyword)
    
    keyword_count = len(found_keywords)
    
    if keyword_count == 0:
        return {
            "score": 0,
            "reason": "No suspicious keywords detected"
        }
    elif keyword_count <= 2:
        return {
            "score": 15,
            "reason": f"Contains suspicious keywords: {', '.join(found_keywords)}"
        }
    else:
        return {
            "score": 30,
            "reason": f"Contains multiple suspicious keywords: {', '.join(found_keywords[:5])}"
        }


def check_tld(url: str) -> Dict[str, Any]:
    """
    Check for unusual or suspicious top-level domains.
    
    Scoring:
    - Standard TLD: 0 points
    - Suspicious TLD: 25 points
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dict with score and reason
    """
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or parsed.netloc.split(':')[0]
        
        if not hostname:
            return {
                "score": 0,
                "reason": "Could not determine TLD"
            }
        
        for suspicious_tld in SUSPICIOUS_TLDS:
            if hostname.endswith(suspicious_tld):
                return {
                    "score": 25,
                    "reason": f"URL uses suspicious TLD: {suspicious_tld}"
                }
        
        return {
            "score": 0,
            "reason": "URL uses standard TLD"
        }
    except Exception:
        return {
            "score": 0,
            "reason": "Could not parse URL"
        }


def check_port(url: str) -> Dict[str, Any]:
    """
    Check for non-standard ports in URL.
    
    Scoring:
    - No port or standard ports (80, 443, 8080): 0 points
    - Non-standard port: 20 points
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dict with score and reason
    """
    try:
        parsed = urlparse(url)
        port = parsed.port
        
        if port is None:
            return {
                "score": 0,
                "reason": "URL uses default port"
            }
        
        standard_ports = [80, 443, 8080]
        if port in standard_ports:
            return {
                "score": 0,
                "reason": f"URL uses standard port {port}"
            }
        
        return {
            "score": 20,
            "reason": f"URL uses uncommon port {port}"
        }
    except Exception:
        return {
            "score": 0,
            "reason": "Could not parse URL"
        }


def calculate_rule_score(url: str) -> Dict[str, Any]:
    """
    Calculate comprehensive rule-based risk score for URL.
    
    Combines all rule checks and returns detailed analysis.
    Maximum possible score: 145 points (normalized to 100)
    
    Args:
        url: The URL to analyze
        
    Returns:
        Dict containing:
        - total_score: Normalized score 0-100
        - checks: Individual check results
    """
    checks = {
        "url_length": analyze_url_length(url),
        "ip_address": check_ip_address(url),
        "suspicious_keywords": detect_suspicious_keywords(url),
        "unusual_tld": check_tld(url),
        "uncommon_port": check_port(url)
    }
    
    raw_score = sum(check["score"] for check in checks.values())
    max_possible_score = 145
    normalized_score = min(100, int((raw_score / max_possible_score) * 100))
    
    return {
        "total_score": normalized_score,
        "raw_score": raw_score,
        "checks": checks
    }
