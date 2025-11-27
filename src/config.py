"""Configuration management for the Link Safety Checker."""
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")
GOOGLE_SAFE_BROWSING_API_ENDPOINT = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

CLIENT_ID = "LinkSafetyChecker"
CLIENT_VERSION = "1.0.0"

THREAT_TYPES = [
    "MALWARE",
    "SOCIAL_ENGINEERING",
    "UNWANTED_SOFTWARE",
    "POTENTIALLY_HARMFUL_APPLICATION"
]

PLATFORM_TYPES = ["ANY_PLATFORM"]
THREAT_ENTRY_TYPES = ["URL"]

REQUEST_TIMEOUT = 10
