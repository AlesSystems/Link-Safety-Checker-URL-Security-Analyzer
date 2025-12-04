# tests/test_url_validator.py

import pytest

from src.url_validator import is_valid_url, validate_url, extract_domain


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://example.com",
        "https://sub.domain.co.uk/path?query=1",
    ],
)
def test_is_valid_url_true(url: str) -> None:
    assert is_valid_url(url) is True


@pytest.mark.parametrize(
    "url",
    [
        "example.com",          # şema yok
        "http://",             # domain yok
        "http://exa mple.com", # boşluk
        "not-a-url",
    ],
)
def test_is_valid_url_false(url: str) -> None:
    assert is_valid_url(url) is False


def test_validate_url_missing_scheme() -> None:
    result = validate_url("example.com")
    assert result["is_valid"] is False
    assert any("scheme" in e.lower() for e in result["errors"])


def test_validate_url_missing_domain() -> None:
    result = validate_url("https:///path-only")
    assert result["is_valid"] is False
    assert any("domain" in e.lower() for e in result["errors"])


def test_validate_url_invalid_chars() -> None:
    result = validate_url("https://exa mple.com")
    assert result["is_valid"] is False
    assert any("invalid characters" in e.lower() for e in result["errors"])


def test_validate_url_suspicious_double_slash_warning() -> None:
    result = validate_url("https://example.com//path")
    assert result["is_valid"] is True  # yine de geçerli sayıyoruz
    assert any("multiple '//'" in w.lower() for w in result["warnings"])


def test_extract_domain_basic() -> None:
    assert extract_domain("https://www.google.com/search") == "www.google.com"


def test_extract_domain_with_port() -> None:
    assert extract_domain("http://localhost:8080/path") == "localhost"


def test_extract_domain_invalid_raises() -> None:
    with pytest.raises(ValueError):
        extract_domain("example.com")  # şemasız -> hata