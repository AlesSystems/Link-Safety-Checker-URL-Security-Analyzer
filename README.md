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

- **Desktop GUI Interface**: User-friendly graphical interface built with Tkinter
- **Real-time URL Analysis**: Powered by Google Safe Browsing API v4
- **Threat Detection**: Identifies MALWARE, SOCIAL_ENGINEERING, UNWANTED_SOFTWARE, and POTENTIALLY_HARMFUL_APPLICATION
- **Color-Coded Results**: Visual feedback with green (safe), yellow (suspicious), and red (dangerous) indicators
- **Error Handling**: Comprehensive error messages for API issues, network problems, and configuration errors
- **Background Processing**: Non-blocking UI with threaded API calls
- **Multiple Entry Points**: Both GUI and CLI interfaces available

## 🛠️ How It Works

The URL Safety Checker integrates with Google Safe Browsing API to provide real-time threat analysis:

1. **User Input**: Enter a URL through the GUI or command line
2. **API Request**: The application sends the URL to Google Safe Browsing API v4
3. **Threat Analysis**: Google's database checks for known threats:
   - MALWARE: Sites that install malicious software
   - SOCIAL_ENGINEERING: Phishing sites that trick users
   - UNWANTED_SOFTWARE: Sites that host unwanted applications
   - POTENTIALLY_HARMFUL_APPLICATION: Sites with potentially risky content
4. **Result Classification**: The response is parsed and classified as:
   - **Safe**: No threats detected
   - **Suspicious**: Potentially harmful applications detected
   - **Dangerous**: Malware, phishing, or unwanted software detected
5. **Display**: Results are shown with color-coded visual feedback

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

- Python 3.7 or higher
- tkinter (included in standard Python distribution)
- Internet connection for API calls
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
URL: https://example.com/path?query=value
Status: SAFE ✅
Details:
  - No threats detected
  - Checked at: 2024-11-27T10:30:00Z
```

## 🚦 Security Classifications

| Classification | Description | Threat Types |
|----------------|-------------|--------------|
| **Safe** ✅ | URL appears legitimate with no threats detected | None |
| **Suspicious** ⚠️ | URL contains potentially harmful applications | POTENTIALLY_HARMFUL_APPLICATION |
| **Dangerous** 🚫 | URL contains known malicious content | MALWARE, SOCIAL_ENGINEERING, UNWANTED_SOFTWARE |

### Threat Types Detected

- **MALWARE**: Sites that install malicious software on your device
- **SOCIAL_ENGINEERING**: Phishing sites designed to trick users into revealing sensitive information
- **UNWANTED_SOFTWARE**: Sites that host applications with deceptive behavior
- **POTENTIALLY_HARMFUL_APPLICATION**: Sites with applications that may be risky

### API Integration

This tool uses **Google Safe Browsing API v4**, which protects over 4 billion devices daily. The API checks URLs against Google's constantly updated list of unsafe web resources.

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
