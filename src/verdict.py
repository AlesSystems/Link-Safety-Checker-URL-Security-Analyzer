"""Final security verdict object for URL analysis."""
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class FinalSecurityVerdict:
    """
    Comprehensive security verdict combining API and rule-based analysis.
    
    This class represents the final verdict for a URL check, including:
    - API results from Google Safe Browsing
    - Rule-based risk scoring
    - Combined analysis and reasoning
    """
    
    def __init__(
        self,
        url: str,
        verdict: str,
        api_data: Dict[str, Any],
        rule_based_score: Dict[str, Any],
        reasons: List[str],
        timestamp: Optional[str] = None
    ):
        """
        Initialize final security verdict.
        
        Args:
            url: The checked URL
            verdict: Final classification ('safe', 'suspicious', 'dangerous')
            api_data: Dictionary with API result data
            rule_based_score: Dictionary with rule-based analysis
            reasons: List of human-readable explanations
            timestamp: ISO timestamp (generated if not provided)
        """
        self.url = url
        self.verdict = verdict
        self.api_data = api_data
        self.rule_based_score = rule_based_score
        self.reasons = reasons
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert verdict to dictionary format.
        
        Returns:
            JSON-serializable dictionary
        """
        return {
            "url": self.url,
            "verdict": self.verdict,
            "api_data": self.api_data,
            "rule_based_score": self.rule_based_score,
            "reasons": self.reasons,
            "timestamp": self.timestamp
        }
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert verdict to JSON string.
        
        Args:
            indent: JSON indentation level
            
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent)
    
    def is_safe(self) -> bool:
        """Check if URL is classified as safe."""
        return self.verdict == "safe"
    
    def is_suspicious(self) -> bool:
        """Check if URL is classified as suspicious."""
        return self.verdict == "suspicious"
    
    def is_dangerous(self) -> bool:
        """Check if URL is classified as dangerous."""
        return self.verdict == "dangerous"
    
    def get_summary(self) -> str:
        """
        Get a brief summary of the verdict.
        
        Returns:
            Human-readable summary string
        """
        verdict_emoji = {
            "safe": "✅",
            "suspicious": "⚠️",
            "dangerous": "❌"
        }
        
        emoji = verdict_emoji.get(self.verdict, "❓")
        score = self.rule_based_score.get("total_score", 0)
        api_status = "available" if self.api_data.get("available") else "unavailable"
        
        return f"{emoji} {self.verdict.upper()} | Rule Score: {score}/100 | API: {api_status}"
    
    def __repr__(self) -> str:
        return f"FinalSecurityVerdict(url='{self.url}', verdict='{self.verdict}')"
    
    def __str__(self) -> str:
        return self.get_summary()
