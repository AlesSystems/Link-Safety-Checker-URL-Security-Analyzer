"""Main integration module for complete URL analysis."""
from typing import Optional
from datetime import datetime, timezone

from src.api_client import check_url_safety, SafeBrowsingAPIError
from src.response_parser import parse_safe_browsing_response
from src.risk_scorer import calculate_rule_score
from src.score_combiner import combine_scores
from src.verdict import FinalSecurityVerdict


def analyze_url_complete(url: str) -> FinalSecurityVerdict:
    """
    Perform complete URL security analysis combining API and rule-based checks.
    
    This function:
    1. Checks URL with Google Safe Browsing API
    2. Performs rule-based risk scoring
    3. Combines results into final verdict
    4. Handles API failures gracefully
    
    Args:
        url: The URL to analyze
        
    Returns:
        FinalSecurityVerdict object with comprehensive analysis
    """
    api_result = None
    api_available = True
    
    try:
        api_response = check_url_safety(url)
        api_result = parse_safe_browsing_response(api_response, url)
    except SafeBrowsingAPIError as e:
        api_available = False
        api_result = None
    
    rule_score = calculate_rule_score(url)
    
    verdict_dict = combine_scores(
        api_result=api_result,
        rule_score=rule_score,
        url=url
    )
    
    if not verdict_dict.get("timestamp"):
        verdict_dict["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    return FinalSecurityVerdict(
        url=verdict_dict["url"],
        verdict=verdict_dict["verdict"],
        api_data=verdict_dict["api_data"],
        rule_based_score=verdict_dict["rule_based_score"],
        reasons=verdict_dict["reasons"],
        timestamp=verdict_dict["timestamp"]
    )
