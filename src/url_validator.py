# src/url_validator.py

from urllib.parse import urlparse
import re
from typing import Dict, Any, List

# Geçerli şemalar
VALID_SCHEMES = {"http", "https"}

# URL içinde olmaması gereken karakterler (boşluk, bazı özel karakterler)
INVALID_CHARS_RE = re.compile(r'[\s<>{}|\\^`"]')


def is_valid_url(url: str) -> bool:
    """
    Basit URL doğrulayıcı.
    Geçerli bir http/https URL ise True, değilse False döner.
    """
    result = validate_url(url)
    return result["is_valid"]


def validate_url(url: str) -> Dict[str, Any]:
    """
    URL'yi detaylı kontrol eder, yapılandırılmış sonuç döner.

    Dönen dict örneği:
    {
        "is_valid": True/False,
        "errors": [...],      # Geçersiz yapan hatalar
        "warnings": [...],    # Şüpheli ama kesin hatalı olmayan durumlar
        "scheme": "http",
        "domain": "example.com",
        "url": "http://example.com"
    }
    """
    errors: List[str] = []
    warnings: List[str] = []

    if not url:
        return {
            "is_valid": False,
            "errors": ["Empty URL."],
            "warnings": [],
            "scheme": None,
            "domain": None,
            "url": url,
        }

    try:
        parsed = urlparse(url)
    except Exception as exc:
        return {
            "is_valid": False,
            "errors": [f"Parse error: {exc}"],
            "warnings": [],
            "scheme": None,
            "domain": None,
            "url": url,
        }

    # Şema (scheme) kontrolü
    if not parsed.scheme:
        errors.append("Missing scheme (e.g. http or https).")
    elif parsed.scheme not in VALID_SCHEMES:
        warnings.append(f"Suspicious scheme: {parsed.scheme}")

    # Domain (netloc) kontrolü
    if not parsed.netloc:
        errors.append("Missing domain (host).")

    # Geçersiz karakter kontrolü
    if INVALID_CHARS_RE.search(url):
        errors.append("URL contains invalid characters (whitespace or control chars).")

    # Birden fazla '//' kullanımı (şüpheli pattern)
    raw = url
    if "://" in raw:
        after_scheme = raw.split("://", 1)[1]
        if "//" in after_scheme:
            warnings.append("URL contains multiple '//' segments after the scheme, which is suspicious.")
    else:
        if raw.count("//") > 1:
            warnings.append("URL contains multiple '//' segments, which is suspicious.")

    # TLD (son uzantı) için çok kaba kontrol
    host = parsed.netloc.split(":")[0]  # port'u at
    if host:
        if "." not in host:
            warnings.append("Domain has no dot; may be local or invalid.")
        else:
            tld = host.rsplit(".", 1)[1]
            if not (2 <= len(tld) <= 24):
                warnings.append(f"Suspicious top‑level domain: .{tld}")

    is_valid = len(errors) == 0

    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "scheme": parsed.scheme or None,
        "domain": host or None,
        "url": url,
    }


def extract_domain(url: str) -> str:
    """
    Geçerli bir URL'den domain'i döndürür (port hariç).
    Örnek: 'https://sub.example.com:8080/path' -> 'sub.example.com'
    """
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and domain (e.g. 'https://example.com').")
    return parsed.netloc.split(":")[0]