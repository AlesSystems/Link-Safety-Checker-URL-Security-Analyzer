# Link Safety Checker - URL Security Analyzer

A simple URL Safety Checker that analyzes links and determines whether they are **Safe**, **Suspicious**, or **Potentially Dangerous** based on simple heuristics and rules.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Security Classifications](#security-classifications)
- [Contributing](#contributing)
- [Developers](#developers)
- [License](#license)

## 🔍 Overview

This project is designed to help users identify potentially malicious URLs before clicking on them. It uses a set of heuristics and pattern matching to analyze URLs and provide a safety assessment. The tool is perfect for learning URL parsing, security fundamentals, and clean software architecture.

## ✨ Features

- **URL Pattern Analysis**: Detects suspicious patterns commonly found in phishing and malicious URLs
- **Structure Validation**: Checks for unsafe URL structures and malformed components
- **Redirect Detection**: Identifies potential redirect chains that may lead to malicious sites
- **Domain Analysis**: Examines domain names for suspicious characteristics
- **IP Address Detection**: Flags URLs using raw IP addresses instead of domain names
- **Special Character Detection**: Identifies excessive use of special characters often used in obfuscation
- **URL Length Analysis**: Flags unusually long URLs that may indicate malicious intent
- **Subdomain Analysis**: Detects excessive subdomains often used in phishing attacks

## 🛠️ How It Works

The URL Safety Checker analyzes URLs using the following heuristics:

1. **Protocol Check**: Verifies if the URL uses secure protocols (HTTPS vs HTTP)
2. **Domain Reputation**: Checks against known suspicious domain patterns
3. **Path Analysis**: Examines URL paths for suspicious keywords and patterns
4. **Query String Inspection**: Analyzes query parameters for potential injection attempts
5. **Encoding Detection**: Identifies URL encoding that may be used to hide malicious content
6. **Homograph Detection**: Checks for characters that look similar to legitimate domain characters

## 📦 Requirements

### Functional Requirements

1. **URL Input**: Accept URLs from users for analysis
2. **URL Parsing**: Parse and decompose URLs into their components (protocol, domain, path, query, fragment)
3. **Pattern Matching**: Implement pattern matching algorithms to detect suspicious patterns
4. **Risk Assessment**: Calculate a risk score based on multiple heuristics
5. **Result Output**: Display clear safety classification and detailed analysis results
6. **Batch Processing**: Support analyzing multiple URLs at once

### Non-Functional Requirements

1. **Performance**: Analyze URLs within milliseconds for responsive user experience
2. **Accuracy**: Minimize false positives while maintaining high detection rates
3. **Usability**: Provide clear, understandable results for non-technical users
4. **Extensibility**: Design architecture to easily add new heuristics and rules
5. **Maintainability**: Follow clean code principles for easy maintenance

### Technical Requirements

- Modern web browser or command-line interface
- No external API dependencies for basic functionality
- Cross-platform compatibility

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/AlesSystems/Link-Safety-Checker-URL-Security-Analyzer.git
```

2. Navigate to the project directory:
```bash
cd Link-Safety-Checker-URL-Security-Analyzer
```

3. Follow language-specific setup instructions (to be added based on implementation)

## 📖 Usage

### Basic Usage

```
# Example usage (syntax depends on implementation)
check-url "https://example.com/path?query=value"
```

### Expected Output

```
URL: https://example.com/path?query=value
Status: SAFE ✅
Risk Score: 0/100
Details:
  - Protocol: HTTPS (Secure)
  - Domain: Legitimate pattern
  - Path: No suspicious keywords
  - Query: Clean parameters
```

## 🚦 Security Classifications

| Classification | Description | Risk Score |
|----------------|-------------|------------|
| **Safe** ✅ | URL appears legitimate with no suspicious indicators | 0-30 |
| **Suspicious** ⚠️ | URL contains some concerning patterns, proceed with caution | 31-70 |
| **Potentially Dangerous** 🚫 | URL shows strong indicators of malicious intent | 71-100 |

### Common Risk Indicators

- Use of IP address instead of domain name
- Presence of @ symbol in URL (credential injection)
- Excessive subdomains (e.g., login.secure.bank.suspicious.com)
- Known phishing keywords (login, secure, verify, update, account)
- URL shortener services
- Misspelled common domain names (homograph attacks)
- Non-standard port numbers
- Excessive URL length
- Multiple redirects in query parameters

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Developers

This project is developed and maintained by:

- **Altan Esmer**
- **Kayra Yetis**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ If you find this project helpful, please consider giving it a star!
