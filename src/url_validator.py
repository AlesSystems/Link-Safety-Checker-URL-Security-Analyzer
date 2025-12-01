"""URL validation and formatting module for Link Safety Checker."""
import re
from urllib.parse import urlparse, urlunparse
from typing import Dict, List, Any


class URLValidationResult:
    """Result object for URL validation."""
    
    def __init__(self, is_valid: bool, formatted_url: str = "", 
                 errors: List[str] = None, warnings: List[str] = None,
                 suggestions: List[str] = None):
        """Initialize validation result.
        
        Args:
            is_valid: Whether the URL is valid
            formatted_url: Auto-formatted URL with proper protocol
            errors: List of validation errors
            warnings: List of validation warnings
            suggestions: List of correction suggestions
        """
        self.is_valid = is_valid
        self.formatted_url = formatted_url
        self.errors = errors or []
        self.warnings = warnings or []
        self.suggestions = suggestions or []


class URLValidator:
    """URL validation and formatting utilities."""
    
    # Suspicious TLDs (commonly used in phishing)
    SUSPICIOUS_TLDS = {
        '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club',
        '.work', '.date', '.racing', '.download', '.stream', '.review'
    }
    
    # Common domain typos
    COMMON_DOMAINS = {
        'gogle': 'google',
        'googel': 'google',
        'gooogle': 'google',
        'yahooo': 'yahoo',
        'facbook': 'facebook',
        'facebok': 'facebook',
        'amazom': 'amazon',
        'amzon': 'amazon',
        'paypa1': 'paypal',
        'paypai': 'paypal',
        'twiter': 'twitter',
        'twtter': 'twitter',
        'linkedim': 'linkedin',
        'linkdin': 'linkedin'
    }
    
    @staticmethod
    def validate_url(url: str) -> URLValidationResult:
        """Validate URL format and check for suspicious patterns.
        
        Args:
            url: URL string to validate
            
        Returns:
            URLValidationResult object with validation details
        """
        errors = []
        warnings = []
        suggestions = []
        
        if not url or not url.strip():
            return URLValidationResult(
                is_valid=False,
                errors=["URL cannot be empty"],
                suggestions=["Please enter a valid URL"]
            )
        
        url = url.strip()
        
        # Try to format URL (add protocol if missing)
        formatted_url = URLValidator.format_url(url)
        
        # Parse URL
        try:
            parsed = urlparse(formatted_url)
            
            # Check for valid scheme
            if not parsed.scheme:
                errors.append("Missing protocol (http:// or https://)")
                suggestions.append("Add 'https://' at the beginning")
            elif parsed.scheme not in ['http', 'https']:
                errors.append(f"Invalid protocol: {parsed.scheme}")
                suggestions.append("Use 'http://' or 'https://' protocol")
            
            # Check for valid domain/hostname
            if not parsed.netloc:
                errors.append("Missing domain name")
                suggestions.append("Enter a complete URL like 'https://example.com'")
            else:
                # Check if IP address is used instead of domain
                if URLValidator._is_ip_address(parsed.netloc):
                    warnings.append("URL uses IP address instead of domain name")
                    warnings.append("This is unusual and may indicate a suspicious site")
                
                # Check for suspicious TLDs
                for tld in URLValidator.SUSPICIOUS_TLDS:
                    if parsed.netloc.endswith(tld):
                        warnings.append(f"Suspicious top-level domain: {tld}")
                        warnings.append("This TLD is commonly used in phishing attacks")
                        break
                
                # Check for unusual ports
                if parsed.port and parsed.port not in [80, 443, 8080, 8443]:
                    warnings.append(f"Unusual port number: {parsed.port}")
                    warnings.append("Standard ports are 80 (HTTP) and 443 (HTTPS)")
                
                # Check for domain typos
                domain_parts = parsed.netloc.split('.')
                if len(domain_parts) >= 2:
                    main_domain = domain_parts[-2].lower()
                    if main_domain in URLValidator.COMMON_DOMAINS:
                        correct_domain = URLValidator.COMMON_DOMAINS[main_domain]
                        suggestions.append(f"Did you mean '{correct_domain}.{domain_parts[-1]}'?")
                        warnings.append(f"Possible typo in domain name: {main_domain}")
            
            # Check for suspicious patterns in path
            if parsed.path:
                suspicious_patterns = [
                    'login', 'signin', 'verify', 'account', 'secure',
                    'update', 'confirm', 'banking', 'paypal'
                ]
                path_lower = parsed.path.lower()
                for pattern in suspicious_patterns:
                    if pattern in path_lower:
                        warnings.append(f"URL contains '{pattern}' - verify authenticity")
                        break
            
            # URL is valid if no errors
            is_valid = len(errors) == 0
            
            return URLValidationResult(
                is_valid=is_valid,
                formatted_url=formatted_url,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions
            )
            
        except Exception as e:
            return URLValidationResult(
                is_valid=False,
                errors=[f"Invalid URL format: {str(e)}"],
                suggestions=["Check the URL format and try again"]
            )
    
    @staticmethod
    def format_url(url: str) -> str:
        """Auto-format URL by adding protocol if missing.
        
        Args:
            url: URL string to format
            
        Returns:
            Formatted URL with proper protocol
        """
        url = url.strip()
        
        # Check if URL already has a protocol
        if url.startswith('http://') or url.startswith('https://'):
            return url
        
        # Check if it starts with www or looks like a domain
        if url.startswith('www.') or '.' in url:
            # Prefer HTTPS over HTTP
            return f"https://{url}"
        
        # If it doesn't look like a URL, still try to make it work
        return f"https://{url}"
    
    @staticmethod
    def _is_ip_address(hostname: str) -> bool:
        """Check if hostname is an IP address.
        
        Args:
            hostname: Hostname to check
            
        Returns:
            True if hostname is an IP address, False otherwise
        """
        # Remove port if present
        host = hostname.split(':')[0]
        
        # Check for IPv4
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ipv4_pattern, host):
            # Validate that each octet is 0-255
            parts = host.split('.')
            try:
                return all(0 <= int(part) <= 255 for part in parts)
            except ValueError:
                return False
        
        # Check for IPv6 (simplified check)
        if ':' in host and '[' not in hostname:  # IPv6 without brackets
            return True
        if '[' in hostname and ']' in hostname:  # IPv6 with brackets
            return True
        
        return False
    
    @staticmethod
    def suggest_corrections(url: str) -> List[str]:
        """Suggest corrections for common URL mistakes.
        
        Args:
            url: URL to analyze
            
        Returns:
            List of suggested corrections
        """
        suggestions = []
        
        # Check for missing protocol
        if not url.startswith('http://') and not url.startswith('https://'):
            suggestions.append(f"Add protocol: https://{url}")
        
        # Check for common typos
        for typo, correct in URLValidator.COMMON_DOMAINS.items():
            if typo in url.lower():
                corrected_url = url.lower().replace(typo, correct)
                suggestions.append(f"Possible typo fix: {corrected_url}")
        
        return suggestions
