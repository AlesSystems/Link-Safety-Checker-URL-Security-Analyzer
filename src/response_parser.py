"""Parser for Google Safe Browsing API responses."""
from typing import Dict, Any, List
from datetime import datetime, timezone


class URLSafetyResult:
    """Represents the safety status of a checked URL."""
    
    def __init__(self, url: str, status: str, threat_types: List[str] = None, 
                 raw_response: Dict[str, Any] = None):
        """
        Initialize URL safety result.
        
        Args:
            url: The URL that was checked
            status: Classification status ('safe', 'suspicious', 'dangerous')
            threat_types: List of detected threat types
            raw_response: Original API response for debugging
        """
        self.url = url
        self.status = status
        self.threat_types = threat_types or []
        self.raw_response = raw_response
        self.timestamp = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary format."""
        return {
            "url": self.url,
            "status": self.status,
            "threat_types": self.threat_types,
            "timestamp": self.timestamp,
            "raw_response": self.raw_response
        }
    
    def __repr__(self) -> str:
        return f"URLSafetyResult(url='{self.url}', status='{self.status}', threat_types={self.threat_types})"


def parse_safe_browsing_response(api_response: Dict[str, Any], url: str) -> URLSafetyResult:
    """
    Parse Google Safe Browsing API response and classify URL safety.
    
    Mapping rules:
    - Empty response or no matches -> 'safe'
    - MALWARE, UNWANTED_SOFTWARE -> 'dangerous'
    - SOCIAL_ENGINEERING (Phishing) -> 'dangerous'
    - POTENTIALLY_HARMFUL_APPLICATION -> 'suspicious'
    
    Args:
        api_response: Raw JSON response from Google Safe Browsing API
        url: The URL that was checked
        
    Returns:
        URLSafetyResult object with classification and details
    """
    if not api_response:
        return URLSafetyResult(
            url=url,
            status="safe",
            threat_types=[],
            raw_response=api_response
        )
    
    matches = api_response.get("matches", [])
    
    if not matches:
        return URLSafetyResult(
            url=url,
            status="safe",
            threat_types=[],
            raw_response=api_response
        )
    
    threat_types = []
    for match in matches:
        threat_type = match.get("threatType")
        if threat_type and threat_type not in threat_types:
            threat_types.append(threat_type)
    
    dangerous_threats = {"MALWARE", "UNWANTED_SOFTWARE", "SOCIAL_ENGINEERING"}
    suspicious_threats = {"POTENTIALLY_HARMFUL_APPLICATION"}
    
    detected_dangerous = any(threat in dangerous_threats for threat in threat_types)
    detected_suspicious = any(threat in suspicious_threats for threat in threat_types)
    
    if detected_dangerous:
        status = "dangerous"
    elif detected_suspicious:
        status = "suspicious"
    else:
        status = "suspicious"
    
    return URLSafetyResult(
        url=url,
        status=status,
        threat_types=threat_types,
        raw_response=api_response
    )
