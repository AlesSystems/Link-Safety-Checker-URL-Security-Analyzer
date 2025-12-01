"""
Visual Test for Features 4 & 5
Run this file to see the new features in action.
"""
import tkinter as tk
from datetime import datetime, timezone
from src.gui import LinkSafetyCheckerGUI

# Mock verdict object for testing
class MockVerdict:
    def __init__(self):
        self.verdict = "suspicious"
        self.url = "https://example-suspicious.com"
        self.timestamp = datetime.now(timezone.utc).isoformat()
        
        # Mock API data
        self.api_data = {
            'available': True,
            'threat_types': ['SOCIAL_ENGINEERING', 'POTENTIALLY_HARMFUL_APPLICATION'],
            'raw_response': {
                'matches': [
                    {
                        'threatType': 'SOCIAL_ENGINEERING',
                        'platformType': 'ANY_PLATFORM',
                        'threatEntryType': 'URL',
                        'cacheDuration': '300s'
                    },
                    {
                        'threatType': 'POTENTIALLY_HARMFUL_APPLICATION',
                        'platformType': 'WINDOWS',
                        'threatEntryType': 'URL',
                        'cacheDuration': '300s'
                    }
                ]
            }
        }
        
        # Mock rule-based score
        self.rule_based_score = {
            'total_score': 65,
            'components': {
                'domain_age': 20,
                'suspicious_patterns': 25,
                'url_length': 10,
                'https_check': -5
            },
            'risk_factors': [
                'Suspicious domain pattern detected',
                'Multiple threat types found',
                'Domain registered recently'
            ]
        }
        
        # Mock reasons
        self.reasons = [
            'Multiple threat types detected by API',
            'Suspicious URL patterns identified',
            'High risk score from rule-based analysis'
        ]

def test_features():
    """Test Features 4 & 5 with mock data."""
    root = tk.Tk()
    app = LinkSafetyCheckerGUI(root)
    
    # Simulate a scan result
    print("\n" + "="*60)
    print("TESTING FEATURES 4 & 5")
    print("="*60)
    
    # Set URL
    app.url_var.set("https://example-suspicious.com")
    
    # Create mock verdict
    verdict = MockVerdict()
    
    # Display result (this will show Feature 5: Timestamp)
    print("\n✓ Testing Feature 5: Timestamp Display")
    print("  - Absolute timestamp format")
    print("  - Relative time calculation")
    app.display_result(verdict)
    
    print("\n✓ Testing Feature 4: Detailed Threat Information")
    print("  - Tree structure display")
    print("  - API analysis section")
    print("  - Rule-based analysis section")
    print("  - Final verdict section")
    
    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("="*60)
    print("1. The GUI window has opened with a mock scan result")
    print("2. Look for the timestamp below the result (Feature 5)")
    print("3. Click 'View Details' button to see detailed analysis (Feature 4)")
    print("4. Scroll through the detailed threat information")
    print("5. Click 'Hide Details' to collapse the section")
    print("6. Click 'Copy Result' to test timestamp in copied text")
    print("7. Close the window when done testing")
    print("="*60 + "\n")
    
    root.mainloop()

if __name__ == "__main__":
    test_features()
