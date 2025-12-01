"""Score combination logic for merging API and rule-based results."""
from typing import Dict, Any, List, Optional
from src.response_parser import URLSafetyResult


def determine_final_verdict(
    api_status: Optional[str],
    rule_score: int,
    api_available: bool
) -> str:
    """
    Determine final verdict based on API status and rule score.
    
    Algorithm:
    - API dangerous OR rule_score > 60 -> dangerous
    - API suspicious OR (API safe but rule_score 30-60) -> suspicious
    - API safe AND rule_score < 30 -> safe
    - API unavailable -> use rule_score only
    
    Args:
        api_status: API classification ('safe', 'suspicious', 'dangerous')
        rule_score: Rule-based score (0-100)
        api_available: Whether API was available
        
    Returns:
        Final verdict string
    """
    if not api_available:
        if rule_score > 60:
            return "dangerous"
        elif rule_score >= 30:
            return "suspicious"
        else:
            return "safe"
    
    if api_status == "dangerous" or rule_score > 60:
        return "dangerous"
    
    if api_status == "suspicious" or (api_status == "safe" and rule_score >= 30):
        return "suspicious"
    
    return "safe"


def generate_reasons(
    api_result: Optional[URLSafetyResult],
    rule_score: Dict[str, Any],
    api_available: bool
) -> List[str]:
    """
    Generate human-readable explanations for the verdict.
    
    Args:
        api_result: Result from Google Safe Browsing API
        rule_score: Rule-based score dictionary
        api_available: Whether API was available
        
    Returns:
        List of reason strings
    """
    reasons = []
    
    if api_available and api_result:
        if api_result.threat_types:
            threat_list = ", ".join(api_result.threat_types)
            reasons.append(f"Google Safe Browsing detected threats: {threat_list}")
        elif api_result.status == "safe":
            reasons.append("Google Safe Browsing reports no known threats")
    else:
        reasons.append("Google Safe Browsing API unavailable - using rule-based analysis only")
    
    checks = rule_score.get("checks", {})
    for check_name, check_result in checks.items():
        if check_result.get("score", 0) > 0:
            reasons.append(check_result.get("reason", ""))
    
    if not reasons:
        reasons.append("No security concerns detected")
    
    return reasons


def combine_scores(
    api_result: Optional[URLSafetyResult],
    rule_score: Dict[str, Any],
    url: str
) -> Dict[str, Any]:
    """
    Combine API result and rule-based score into final verdict.
    
    Weighting:
    - API Result: 70% (primary source)
    - Rule-Based Score: 30% (secondary validation)
    
    Args:
        api_result: Result from Google Safe Browsing API (None if unavailable)
        rule_score: Rule-based score dictionary
        url: The checked URL
        
    Returns:
        Final verdict dictionary with all analysis data
    """
    api_available = api_result is not None
    api_status = api_result.status if api_result else None
    
    final_verdict = determine_final_verdict(
        api_status=api_status,
        rule_score=rule_score.get("total_score", 0),
        api_available=api_available
    )
    
    reasons = generate_reasons(
        api_result=api_result,
        rule_score=rule_score,
        api_available=api_available
    )
    
    api_data = {
        "status": api_status,
        "threat_types": api_result.threat_types if api_result else [],
        "available": api_available
    }
    
    timestamp = api_result.timestamp if api_result else None
    
    return {
        "url": url,
        "verdict": final_verdict,
        "api_data": api_data,
        "rule_based_score": rule_score,
        "reasons": reasons,
        "timestamp": timestamp
    }
