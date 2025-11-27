"""Example usage of the Link Safety Checker API integration."""
from src.api_client import check_url_safety, APIKeyError, RateLimitError, NetworkError
from src.response_parser import parse_safe_browsing_response


def main():
    """Demonstrate URL safety checking."""
    # Example URLs to check
    test_urls = [
        "https://google.com",
        "https://example.com",
    ]
    
    print("Link Safety Checker - Example Usage")
    print("=" * 50)
    print()
    
    for url in test_urls:
        try:
            print(f"Checking URL: {url}")
            
            # Step 1: Call the API
            api_response = check_url_safety(url)
            
            # Step 2: Parse the response
            result = parse_safe_browsing_response(api_response, url)
            
            # Step 3: Display results
            print(f"  Status: {result.status.upper()}")
            if result.threat_types:
                print(f"  Threats detected: {', '.join(result.threat_types)}")
            else:
                print(f"  No threats detected")
            print(f"  Checked at: {result.timestamp}")
            print()
            
        except APIKeyError as e:
            print(f"  ❌ API Key Error: {e}")
            print(f"  Please set your GOOGLE_SAFE_BROWSING_API_KEY in .env file")
            print()
            break
            
        except RateLimitError as e:
            print(f"  ⚠️  Rate Limit Error: {e}")
            print()
            
        except NetworkError as e:
            print(f"  ❌ Network Error: {e}")
            print()
            
        except Exception as e:
            print(f"  ❌ Unexpected Error: {e}")
            print()


if __name__ == "__main__":
    main()
