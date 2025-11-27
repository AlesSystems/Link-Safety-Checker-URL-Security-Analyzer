"""Google Safe Browsing API client for URL safety checks."""
import logging
import requests
from typing import Dict, Any, Optional
from src.config import (
    GOOGLE_SAFE_BROWSING_API_KEY,
    GOOGLE_SAFE_BROWSING_API_ENDPOINT,
    CLIENT_ID,
    CLIENT_VERSION,
    THREAT_TYPES,
    PLATFORM_TYPES,
    THREAT_ENTRY_TYPES,
    REQUEST_TIMEOUT
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SafeBrowsingAPIError(Exception):
    """Base exception for Safe Browsing API errors."""
    pass


class APIKeyError(SafeBrowsingAPIError):
    """Raised when API key is invalid or missing."""
    pass


class RateLimitError(SafeBrowsingAPIError):
    """Raised when rate limit is exceeded."""
    pass


class NetworkError(SafeBrowsingAPIError):
    """Raised when network connection fails."""
    pass


def check_url_safety(url: str) -> Dict[str, Any]:
    """
    Check if a URL is safe using Google Safe Browsing API.
    
    Args:
        url: The URL to check for safety
        
    Returns:
        Dictionary containing the API response with threat information
        
    Raises:
        APIKeyError: When API key is invalid or missing
        RateLimitError: When rate limit is exceeded
        NetworkError: When network connection fails
        SafeBrowsingAPIError: For other API-related errors
    """
    if not GOOGLE_SAFE_BROWSING_API_KEY:
        logger.error("API key is not configured")
        raise APIKeyError("Google Safe Browsing API key is not configured. Please set GOOGLE_SAFE_BROWSING_API_KEY environment variable.")
    
    request_body = {
        "client": {
            "clientId": CLIENT_ID,
            "clientVersion": CLIENT_VERSION
        },
        "threatInfo": {
            "threatTypes": THREAT_TYPES,
            "platformTypes": PLATFORM_TYPES,
            "threatEntryTypes": THREAT_ENTRY_TYPES,
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    api_url = f"{GOOGLE_SAFE_BROWSING_API_ENDPOINT}?key={GOOGLE_SAFE_BROWSING_API_KEY}"
    
    try:
        logger.info(f"Checking URL safety: {url}")
        response = requests.post(
            api_url,
            json=request_body,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Successfully checked URL: {url}")
            return result
        
        elif response.status_code == 400:
            logger.error(f"Bad request - Invalid API key or malformed request: {response.text}")
            raise APIKeyError(f"Invalid API key or malformed request: {response.text}")
        
        elif response.status_code == 403:
            logger.error(f"Forbidden - API key restrictions: {response.text}")
            raise APIKeyError(f"API key restrictions or permissions error: {response.text}")
        
        elif response.status_code == 429:
            logger.error("Rate limit exceeded")
            retry_after = response.headers.get("Retry-After", "unknown")
            raise RateLimitError(f"Rate limit exceeded. Retry after: {retry_after}")
        
        else:
            logger.error(f"Unexpected API response: {response.status_code} - {response.text}")
            raise SafeBrowsingAPIError(f"Unexpected API response: {response.status_code}")
    
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout after {REQUEST_TIMEOUT} seconds")
        raise NetworkError(f"Request timeout after {REQUEST_TIMEOUT} seconds")
    
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Network connection error: {str(e)}")
        raise NetworkError(f"Failed to connect to Safe Browsing API: {str(e)}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        raise SafeBrowsingAPIError(f"Request failed: {str(e)}")
    
    except ValueError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise SafeBrowsingAPIError(f"Failed to parse API response: {str(e)}")
