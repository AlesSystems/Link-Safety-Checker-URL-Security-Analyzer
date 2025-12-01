"""Example usage of the Link Safety Checker with complete analysis."""
import json
from src.url_analyzer import analyze_url_complete
from src.api_client import APIKeyError


def print_detailed_verdict(verdict):
    """Print detailed verdict information."""
    print(f"\n{'='*70}")
    print(f"URL: {verdict.url}")
    print(f"{'='*70}")
    print(f"\n{verdict.get_summary()}\n")
    
    # API Results
    print("📡 API Analysis:")
    if verdict.api_data["available"]:
        print(f"   Status: {verdict.api_data['status']}")
        if verdict.api_data["threat_types"]:
            print(f"   Threats: {', '.join(verdict.api_data['threat_types'])}")
        else:
            print(f"   Threats: None detected")
    else:
        print(f"   Status: Unavailable")
    
    # Rule-based Score
    print(f"\n🔍 Rule-Based Analysis:")
    print(f"   Total Score: {verdict.rule_based_score['total_score']}/100")
    print(f"   Individual Checks:")
    for check_name, check_data in verdict.rule_based_score["checks"].items():
        score = check_data["score"]
        reason = check_data["reason"]
        emoji = "✅" if score == 0 else "⚠️" if score < 25 else "❌"
        print(f"      {emoji} {check_name}: {score} pts - {reason}")
    
    # Reasons
    print(f"\n💡 Analysis Summary:")
    for i, reason in enumerate(verdict.reasons, 1):
        print(f"   {i}. {reason}")
    
    print(f"\n⏰ Timestamp: {verdict.timestamp}")
    print(f"{'='*70}\n")


def print_json_verdict(verdict):
    """Print verdict as formatted JSON."""
    print(json.dumps(verdict.to_dict(), indent=2))


def main():
    """Demonstrate complete URL safety analysis."""
    # Example URLs with various risk profiles
    test_urls = [
        "https://google.com",  # Safe, well-known
        "http://192.168.1.1/secure-login",  # IP address + suspicious keywords
        "https://example.tk",  # Suspicious TLD
        "https://very-long-url.com/" + "a" * 300,  # Long URL
    ]
    
    print("🔒 Link Safety Checker - Complete Analysis Demo")
    print("="*70)
    print("\nThis demo shows the new Risk Score and Analysis feature!")
    print("Combining Google Safe Browsing API with rule-based analysis.\n")
    
    for url in test_urls:
        try:
            # Perform complete analysis
            verdict = analyze_url_complete(url)
            
            # Display detailed results
            print_detailed_verdict(verdict)
            
        except APIKeyError as e:
            print(f"\n❌ API Key Error: {e}")
            print(f"Note: Analysis will continue with rule-based scoring only.\n")
            
            # Still analyze with rules only
            verdict = analyze_url_complete(url)
            print_detailed_verdict(verdict)
            
        except Exception as e:
            print(f"\n❌ Unexpected Error analyzing {url}: {e}\n")
    
    # Show JSON output example
    print("\n" + "="*70)
    print("JSON Output Example (for CLI integration):")
    print("="*70)
    try:
        verdict = analyze_url_complete("https://example.com")
        print_json_verdict(verdict)
    except:
        pass


if __name__ == "__main__":
    main()
