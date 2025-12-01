# Link Safety Checker - URL Security Analyzer

A comprehensive URL Safety Checker that analyzes links using **Google Safe Browsing API** combined with **intelligent rule-based heuristics** to determine whether they are **Safe**, **Suspicious**, or **Potentially Dangerous**.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Security Classifications](#security-classifications)
- [Rule-Based Analysis](#rule-based-analysis)
- [Contributing](#contributing)
- [Developers](#developers)
- [License](#license)

## 🔍 Overview

This project is designed to help users identify potentially malicious URLs before clicking on them. It combines the power of Google Safe Browsing API with advanced rule-based heuristics to provide comprehensive URL security analysis. The tool is perfect for learning URL parsing, security fundamentals, and clean software architecture.

## ✨ Features

### Core Features
- **Hybrid Analysis**: Combines Google Safe Browsing API with rule-based scoring
- **Desktop GUI Interface**: User-friendly graphical interface built with Tkinter
- **Real-time URL Analysis**: Powered by Google Safe Browsing API v4
- **Rule-Based Heuristics**: Local pattern analysis for comprehensive threat detection
- **Offline Capability**: Can analyze URLs even when API is unavailable
- **Defense in Depth**: Multiple layers of security analysis

### Analysis Capabilities
- **Threat Detection**: Identifies MALWARE, SOCIAL_ENGINEERING, UNWANTED_SOFTWARE, and POTENTIALLY_HARMFUL_APPLICATION
- **URL Pattern Analysis**: Detects suspicious URL characteristics:
  - Excessive URL length (obfuscation detection)
  - IP address usage instead of domain names
  - Suspicious keywords (phishing indicators)
  - Unusual top-level domains (TLDs)
  - Non-standard ports
- **Risk Scoring**: 0-100 risk score with detailed explanations
- **Transparent Analysis**: Clear reasoning for each security verdict

### User Experience
- **Color-Coded Results**: Visual feedback with green (safe), yellow (suspicious), and red (dangerous) indicators
- **Detailed Explanations**: Users understand WHY a URL is flagged
- **Error Handling**: Comprehensive error messages for API issues, network problems, and configuration errors
- **Background Processing**: Non-blocking UI with threaded API calls
- **Multiple Entry Points**: Both GUI and CLI interfaces available

## 🛠️ How It Works

The URL Safety Checker uses a **hybrid approach** combining API and rule-based analysis:

### Step 1: User Input
Enter a URL through the GUI or command line interface.

### Step 2: Google Safe Browsing API Check (70% Weight)
The application sends the URL to Google Safe Browsing API v4 which checks for:
- **MALWARE**: Sites that install malicious software
- **SOCIAL_ENGINEERING**: Phishing sites that trick users
- **UNWANTED_SOFTWARE**: Sites that host unwanted applications
- **POTENTIALLY_HARMFUL_APPLICATION**: Sites with potentially risky content

### Step 3: Rule-Based Heuristic Analysis (30% Weight)
Simultaneously, the system performs local checks:
1. **URL Length Check**: Detects obfuscated or excessively long URLs
2. **IP Address Detection**: Flags URLs using IP addresses instead of domain names
3. **Suspicious Keywords**: Identifies phishing-related terms (login, verify, account, etc.)
4. **TLD Analysis**: Detects high-risk top-level domains (.tk, .ml, .xyz, etc.)
5. **Port Analysis**: Flags non-standard network ports

### Step 4: Score Combination
The system combines API results (70%) with rule-based score (30%):
- **Dangerous**: API dangerous OR rule score > 60
- **Suspicious**: API suspicious OR (API safe but rule score 30-60)
- **Safe**: API safe AND rule score < 30
- **API Unavailable**: Falls back to rule-based analysis only

### Step 5: Display Results
Results shown with color-coded visual feedback and detailed explanations.

## 📦 Requirements

### Functional Requirements

1. **URL Input**: Accept URLs from users for analysis
2. **URL Parsing**: Parse and decompose URLs into their components (protocol, domain, path, query, fragment)
3. **Pattern Matching**: Implement pattern matching algorithms to detect suspicious patterns
4. **Risk Assessment**: Calculate a risk score based on multiple heuristics
5. **Result Output**: Display clear safety classification and detailed analysis results
6. **API Integration**: Integrate with Google Safe Browsing API for threat intelligence
7. **Offline Mode**: Provide analysis even when API is unavailable

### Non-Functional Requirements

1. **Performance**: Analyze URLs within seconds for responsive user experience
2. **Accuracy**: Minimize false positives while maintaining high detection rates
3. **Usability**: Provide clear, understandable results for non-technical users
4. **Extensibility**: Design architecture to easily add new heuristics and rules
5. **Maintainability**: Follow clean code principles for easy maintenance
6. **Reliability**: Graceful degradation when API is unavailable

### Technical Requirements

- Python 3.7 or higher
- tkinter (included in standard Python distribution)
- requests library for API calls
- Internet connection for API calls (optional for rule-based analysis)
- Google Safe Browsing API key (free tier available)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/AlesSystems/Link-Safety-Checker-URL-Security-Analyzer.git
```

2. Navigate to the project directory:
```bash
cd Link-Safety-Checker-URL-Security-Analyzer
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your Google Safe Browsing API key:
   - Copy `.env.example` to `.env`
   - Add your API key: `GOOGLE_SAFE_BROWSING_API_KEY=your_key_here`
   - Get a free API key from [Google Cloud Console](https://console.cloud.google.com/)

5. Run the application:
```bash
python src/gui.py
```

## 📖 Usage

### GUI Application (Recommended)

Launch the graphical user interface:

```bash
python src/gui.py
```

The GUI provides an intuitive interface where you can:
1. Paste or type a URL in the input field
2. Click "Analyze Link" or press Enter
3. View the safety status with color-coded results:
   - ✅ **Safe** (Green): No threats detected
   - ⚠️ **Suspicious** (Yellow): Potential threats, proceed with caution
   - ⛔ **DANGEROUS** (Red): Do NOT visit this link

### Command Line Usage

You can also use the example script for batch processing:

```bash
python example.py
```

### Expected Output

```
======================================================================
URL: http://192.168.1.1/secure-login
======================================================================

⚠️  SUSPICIOUS | Rule Score: 45/100 | API: available

📡 API Analysis:
   Status: safe
   Threats: None detected

🔍 Rule-Based Analysis:
   Total Score: 45/100
   Individual Checks:
      ✅ url_length: 0 pts - URL length is normal (34 characters)
      ❌ ip_address: 30 pts - URL uses IP address (192.168.1.1) instead of domain name
      ⚠️  suspicious_keywords: 15 pts - Contains suspicious keywords: secure, login
      ✅ unusual_tld: 0 pts - Could not determine TLD
      ✅ uncommon_port: 0 pts - URL uses default port

💡 Analysis Summary:
   1. Google Safe Browsing reports no known threats
   2. URL uses IP address (192.168.1.1) instead of domain name
   3. Contains suspicious keywords: secure, login

⏰ Timestamp: 2024-12-01T10:30:00Z
======================================================================
```

## 🚦 Security Classifications

| Classification | Description | Conditions |
|----------------|-------------|------------|
| **Safe** ✅ | URL appears legitimate with no threats detected | API safe + Rule score < 30 |
| **Suspicious** ⚠️ | URL contains concerning patterns or potential threats | API suspicious OR (API safe + Rule score 30-60) |
| **Dangerous** 🚫 | URL contains known malicious content or high-risk patterns | API dangerous OR Rule score > 60 |

### Threat Types Detected by API

- **MALWARE**: Sites that install malicious software on your device
- **SOCIAL_ENGINEERING**: Phishing sites designed to trick users into revealing sensitive information
- **UNWANTED_SOFTWARE**: Sites that host applications with deceptive behavior
- **POTENTIALLY_HARMFUL_APPLICATION**: Sites with applications that may be risky

### API Integration

This tool uses **Google Safe Browsing API v4**, which protects over 4 billion devices daily. The API checks URLs against Google's constantly updated list of unsafe web resources.

## 🔍 Rule-Based Analysis

The system performs five key rule-based checks:

### 1. URL Length Check
- **0-200 chars**: Normal (0 pts)
- **201-500 chars**: Suspicious (20 pts)
- **501+ chars**: Very suspicious (40 pts)
- **Rationale**: Phishing URLs often use long paths to obfuscate content

### 2. IP Address Detection
- **Domain name**: Normal (0 pts)
- **IP address**: Suspicious (30 pts)
- **Rationale**: Legitimate sites use domain names; IPs indicate temporary infrastructure

### 3. Suspicious Keywords
- **Keywords detected**: secure, verify, update, account, login, bank, paypal, etc.
- **0 keywords**: Normal (0 pts)
- **1-2 keywords**: Concerning (15 pts)
- **3+ keywords**: High risk (30 pts)
- **Rationale**: Phishing attempts commonly use these terms

### 4. Unusual TLD Check
- **Standard TLDs**: Normal (0 pts)
- **Suspicious TLDs**: High risk (25 pts)
- **Examples**: .tk, .ml, .ga, .cf, .xyz, .top
- **Rationale**: Free/cheap TLDs are frequently abused

### 5. Port Analysis
- **Standard ports (80, 443, 8080)**: Normal (0 pts)
- **Custom ports**: Suspicious (20 pts)
- **Rationale**: Legitimate sites rarely use custom ports

**Total Score**: Normalized to 0-100 scale

For detailed documentation of all rules, see [docs/risk_rules.md](docs/risk_rules.md).

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
