# Risk Scoring Rules Documentation

## Overview

This document describes the rule-based risk scoring system used to analyze URL safety characteristics. The system complements the Google Safe Browsing API with local heuristic checks that can identify potentially malicious URLs based on common phishing and malware patterns.

## Scoring Methodology

### Overall Approach

The risk scoring system evaluates URLs based on five key characteristics:
1. **URL Length** - Detects obfuscated or excessively long URLs
2. **IP Address Usage** - Flags URLs using IP addresses instead of domain names
3. **Suspicious Keywords** - Identifies common phishing-related terms
4. **Unusual TLDs** - Detects suspicious top-level domains
5. **Uncommon Ports** - Flags non-standard network ports

Each check assigns a point score based on the severity of the finding. The final score is normalized to a 0-100 scale, where:
- **0-29**: Low risk (safe)
- **30-60**: Medium risk (suspicious)
- **61-100**: High risk (dangerous)

### Maximum Scores

| Check | Max Points | Weight |
|-------|------------|--------|
| URL Length | 40 | High |
| IP Address | 30 | High |
| Suspicious Keywords | 30 | High |
| Unusual TLD | 25 | Medium |
| Uncommon Port | 20 | Medium |
| **Total** | **145** | (normalized to 100) |

---

## Rule Descriptions

### 1. URL Length Check

**Purpose**: Phishing and malware URLs often use very long URLs to obfuscate malicious content or hide the true destination.

**Scoring Logic**:
```
0-200 characters    → 0 points  (Normal)
201-500 characters  → 20 points (Suspicious)
501+ characters     → 40 points (Very Suspicious)
```

**Examples**:
- ✅ `https://google.com/search` (26 chars) → 0 points
- ⚠️ `https://example.com/page?redirect=...` (350 chars) → 20 points
- ❌ `https://phishing.com/verify?token=...` (650 chars) → 40 points

**Rationale**: Legitimate websites rarely use extremely long URLs. Attackers often create long URLs to:
- Bypass URL filters
- Hide malicious parameters
- Confuse users examining the link

---

### 2. IP Address Detection

**Purpose**: Legitimate websites use domain names, not raw IP addresses. Direct IP usage is often associated with malicious infrastructure.

**Scoring Logic**:
```
Domain name (e.g., example.com)     → 0 points
IPv4 address (e.g., 192.168.1.1)    → 30 points
IPv6 address (e.g., [2001:db8::1])  → 30 points
```

**Examples**:
- ✅ `https://paypal.com/login` → 0 points (domain name)
- ❌ `http://192.168.1.100/login` → 30 points (IPv4)
- ❌ `http://[fe80::1]/page` → 30 points (IPv6)

**Rationale**:
- Legitimate businesses use memorable domain names
- IP addresses indicate:
  - Temporary or disposable infrastructure
  - Compromised servers
  - Testing/development servers exposed publicly
  - Direct server access attempts

---

### 3. Suspicious Keywords Detection

**Purpose**: Phishing attacks commonly use certain keywords to create urgency or impersonate legitimate services.

**Keyword List**:
```
secure, verify, update, account, login, signin, bank, paypal,
confirm, password, billing, credit, card, security, suspended,
authenticate, wallet, tax, refund
```

**Scoring Logic**:
```
No keywords      → 0 points
1-2 keywords     → 15 points
3+ keywords      → 30 points
```

**Examples**:
- ✅ `https://example.com/about` → 0 points (no keywords)
- ⚠️ `https://example.com/secure-login` → 15 points (2 keywords)
- ❌ `https://example.com/secure-verify-account-login` → 30 points (4 keywords)

**Rationale**: Attackers use these words to:
- Create false sense of urgency ("verify your account now!")
- Impersonate banking/financial services
- Trick users into entering credentials
- Mimic security warnings

**Note**: This check may produce false positives on legitimate banking sites. That's why it's combined with other checks and API results.

---

### 4. Unusual TLD Check

**Purpose**: Certain top-level domains are frequently associated with malicious activity due to being free, unregulated, or poorly monitored.

**Suspicious TLD List**:
```
.tk, .ml, .ga, .cf, .gq          (Free Freenom domains)
.xyz, .top, .work, .click        (Cheap bulk domains)
.link, .country, .stream         (Generic suspicious)
.download, .win, .bid, .racing   (High abuse rate)
```

**Scoring Logic**:
```
Standard TLD (e.g., .com, .org, .net)  → 0 points
Suspicious TLD (listed above)           → 25 points
```

**Examples**:
- ✅ `https://example.com` → 0 points (.com)
- ✅ `https://example.org` → 0 points (.org)
- ❌ `https://example.tk` → 25 points (.tk)
- ❌ `https://example.xyz` → 25 points (.xyz)

**Rationale**:
- Some TLDs offer free domain registration (abused by attackers)
- Certain TLDs have minimal registration requirements
- High historical abuse rates in security reports
- Low trust indicators from major browsers

**Important**: Many legitimate sites use .xyz and other new TLDs. This is why this check is only one factor in the overall assessment.

---

### 5. Uncommon Port Check

**Purpose**: Web traffic normally uses standard ports (80 for HTTP, 443 for HTTPS). Custom ports may indicate:
- Testing servers
- Proxy/tunnel endpoints
- Malicious C&C infrastructure

**Scoring Logic**:
```
No explicit port           → 0 points (uses default)
Port 80, 443, or 8080      → 0 points (standard)
Any other port             → 20 points (uncommon)
```

**Examples**:
- ✅ `https://example.com` → 0 points (default 443)
- ✅ `http://example.com:80` → 0 points (standard)
- ✅ `http://localhost:8080` → 0 points (common dev port)
- ⚠️ `http://example.com:8888` → 20 points (uncommon)
- ❌ `http://example.com:9999` → 20 points (uncommon)

**Rationale**:
- Legitimate websites use standard ports
- Custom ports suggest:
  - Development/staging servers (shouldn't be public)
  - Proxy services
  - Tunneling/backdoor access
  - Command & control servers

---

## Combining with API Results

### Hybrid Approach

The rule-based score is combined with Google Safe Browsing API results using a weighted algorithm:

**Weight Distribution**:
- API Result: **70%** (primary source of truth)
- Rule-Based Score: **30%** (secondary validation)

### Decision Logic

| API Status | Rule Score | Final Verdict |
|------------|------------|---------------|
| Dangerous | Any | **Dangerous** |
| Suspicious | Any | **Suspicious** |
| Safe | < 30 | **Safe** |
| Safe | 30-60 | **Suspicious** ⬆ |
| Safe | > 60 | **Dangerous** ⬆ |
| Unavailable | < 30 | **Safe** |
| Unavailable | 30-60 | **Suspicious** |
| Unavailable | > 60 | **Dangerous** |

⬆ = Escalated from API result based on rules

### Example Scenarios

#### Scenario 1: API Agrees with Rules
```json
{
  "api": "dangerous",
  "rule_score": 75,
  "verdict": "dangerous" ✅
}
```

#### Scenario 2: Rules Escalate Safe API Result
```json
{
  "api": "safe",
  "rule_score": 65,
  "verdict": "dangerous" ⬆
}
```
*URL is not in Google's database yet, but has multiple suspicious characteristics*

#### Scenario 3: API Unavailable, Rules Decide
```json
{
  "api": null,
  "rule_score": 45,
  "verdict": "suspicious"
}
```
*Offline capability - still provides useful analysis*

---

## Benefits of Rule-Based Scoring

### 1. Defense in Depth
Multiple layers of security analysis reduce single points of failure.

### 2. Offline Capability
Can analyze URLs even when API is unavailable or rate-limited.

### 3. Zero-Day Detection
Can flag suspicious patterns before they're added to Google's threat database.

### 4. Transparency
Users understand **why** a URL is flagged (detailed reasons provided).

### 5. Educational Value
Helps users learn to recognize suspicious URL patterns.

### 6. API Cost Reduction
Can pre-filter obviously suspicious URLs before API call (future optimization).

---

## Limitations and False Positives

### Known Limitations

1. **Corporate Intranets**: May use IP addresses legitimately
2. **Development Servers**: Often use uncommon ports
3. **Banking Sites**: Legitimately use security-related keywords
4. **New TLDs**: Some legitimate businesses use .xyz, .tech, etc.
5. **Long URLs**: Some legitimate sites (especially with tracking) have long URLs

### Mitigation Strategy

- **API takes precedence**: API "safe" result prevents false positive escalation
- **Weighted scoring**: No single rule can mark URL as dangerous alone
- **Clear explanations**: Users see exact reasons for flags
- **Conservative thresholds**: Thresholds tuned to minimize false positives

---

## Future Enhancements

Potential improvements for consideration:

1. **Configurable Rules**: Allow users to adjust weights and thresholds
2. **Whitelist Support**: Skip checks for known-good domains
3. **Machine Learning**: Train on historical data for better accuracy
4. **URL Reputation**: Check against crowd-sourced reputation databases
5. **Certificate Validation**: Add HTTPS/SSL certificate checks
6. **Domain Age**: Check WHOIS data for newly registered domains
7. **Redirects**: Follow and analyze redirect chains

---

## Testing and Validation

All rules have comprehensive unit tests covering:
- Normal cases (should pass)
- Suspicious cases (should flag)
- Edge cases (malformed URLs, etc.)

See `tests/test_risk_scorer.py` for complete test suite.

---

## References and Research

- [Google Safe Browsing API Documentation](https://developers.google.com/safe-browsing)
- [OWASP URL Security Guidelines](https://owasp.org)
- [Phishing URL Characteristics Research](https://www.anti-phishing.org)

---

**Last Updated**: 2024-01-01  
**Version**: 1.0  
**Maintainer**: URL Safety Checker Team
