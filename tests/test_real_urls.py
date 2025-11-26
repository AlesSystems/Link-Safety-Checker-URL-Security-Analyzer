"""Interactive script to test Google Safe Browsing API with real URLs."""
import sys
from src.api_client import check_url_safety, APIKeyError, RateLimitError, NetworkError, SafeBrowsingAPIError
from src.response_parser import parse_safe_browsing_response
from src.config import GOOGLE_SAFE_BROWSING_API_KEY


def print_result(url: str, result):
    """Print formatted safety check result."""
    print("\n" + "=" * 70)
    print(f"URL: {url}")
    print("-" * 70)
    print(f"Status: {result.status.upper()}")
    
    if result.status == "safe":
        print("[SAFE] This URL appears to be SAFE")
    elif result.status == "suspicious":
        print("[WARNING] This URL is SUSPICIOUS - proceed with caution")
    elif result.status == "dangerous":
        print("[DANGER] This URL is DANGEROUS - do not visit!")
    
    if result.threat_types:
        print(f"\nThreat Types Detected:")
        for threat in result.threat_types:
            threat_name = threat.replace("_", " ").title()
            print(f"  • {threat_name}")
    else:
        print("\nNo threats detected")
    
    print(f"\nChecked at: {result.timestamp}")
    print("=" * 70 + "\n")


def test_single_url(url: str):
    """Test a single URL and display results."""
    try:
        print(f"\n[CHECKING] URL: {url}")
        print("Please wait...")
        
        # Step 1: Call the API
        api_response = check_url_safety(url)
        
        # Step 2: Parse the response
        result = parse_safe_browsing_response(api_response, url)
        
        # Step 3: Display results
        print_result(url, result)
        
        # Optionally show raw response
        if result.raw_response:
            show_raw = input("Show raw API response? (y/n): ").lower().strip()
            if show_raw == 'y':
                import json
                print("\nRaw API Response:")
                print(json.dumps(result.raw_response, indent=2))
                print()
        
        return True
        
    except APIKeyError as e:
        print(f"\n[ERROR] API Key Error: {e}")
        print("\nTo fix this:")
        print("1. Get your Google Safe Browsing API key from Google Cloud Console")
        print("2. Create a .env file in the project root")
        print("3. Add this line: GOOGLE_SAFE_BROWSING_API_KEY=your_api_key_here")
        print("\nSee docs/api_research.md for detailed setup instructions.")
        return False
        
    except RateLimitError as e:
        print(f"\n[WARNING] Rate Limit Error: {e}")
        print("You've exceeded the API rate limit. Please wait before trying again.")
        return False
        
    except NetworkError as e:
        print(f"\n[ERROR] Network Error: {e}")
        print("Please check your internet connection and try again.")
        return False
        
    except SafeBrowsingAPIError as e:
        print(f"\n[ERROR] API Error: {e}")
        return False
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def interactive_mode():
    """Run in interactive mode to test multiple URLs."""
    print("\n" + "=" * 70)
    print("Link Safety Checker - Real URL Testing")
    print("=" * 70)
    print("\nEnter URLs to check (one per line).")
    print("Type 'quit' or 'exit' to stop, or 'help' for commands.\n")
    
    while True:
        try:
            url = input("Enter URL to check: ").strip()
            
            if not url:
                continue
                
            if url.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
                
            if url.lower() == 'help':
                print("\nCommands:")
                print("  - Enter any URL to check it")
                print("  - 'quit' or 'exit' to stop")
                print("  - 'help' to show this message")
                print()
                continue
            
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                print(f"Added https:// prefix: {url}")
            
            test_single_url(url)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except EOFError:
            print("\n\nGoodbye!")
            break


def batch_mode(urls: list):
    """Test multiple URLs in batch mode."""
    print("\n" + "=" * 70)
    print("Link Safety Checker - Batch Testing")
    print("=" * 70)
    print(f"Testing {len(urls)} URL(s)...\n")
    
    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] ", end="")
        success = test_single_url(url)
        results.append((url, success))
    
    # Summary
    print("\n" + "=" * 70)
    print("BATCH TEST SUMMARY")
    print("=" * 70)
    successful = sum(1 for _, success in results if success)
    print(f"Successfully checked: {successful}/{len(results)} URLs")
    print("=" * 70 + "\n")


def main():
    """Main entry point."""
    # Check if API key is configured
    if not GOOGLE_SAFE_BROWSING_API_KEY:
        print("\n[ERROR] Google Safe Browsing API key is not configured!")
        print("\nTo set up your API key:")
        print("1. Get your API key from Google Cloud Console:")
        print("   https://console.cloud.google.com/apis/credentials")
        print("2. Create a .env file in the project root")
        print("3. Add this line to .env:")
        print("   GOOGLE_SAFE_BROWSING_API_KEY=your_api_key_here")
        print("\nSee docs/api_research.md for detailed instructions.")
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        # Batch mode: test URLs from command line
        urls = sys.argv[1:]
        batch_mode(urls)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()

