# User Guide - New GUI Features

Welcome to the enhanced Link Safety Checker! This guide covers the new features added to improve your experience.

## 🆕 What's New

Four powerful new features have been added:
1. **Batch URL Scanning** - Analyze multiple URLs at once
2. **Export Results** - Save your scan results in multiple formats
3. **URL Validation** - Real-time validation and auto-formatting
4. **Recent URLs** - Quick access to previously scanned URLs

---

## 📊 Feature 1: Batch URL Scanning

### How to Use:

1. **Switch to Batch Mode:**
   - Click the **"📊 Batch Mode"** button in the input section
   - The interface switches to show a multi-line text area

2. **Enter URLs:**
   - Type or paste multiple URLs (one per line)
   - Example:
     ```
     https://google.com
     https://example.com
     facebook.com
     ```

3. **Start Scanning:**
   - Click the **"📊 ANALYZE BATCH"** button
   - Watch the progress indicator: "Processing 3/10..."

4. **View Results:**
   - Results appear in real-time with status indicators:
     - ✅ Safe
     - ⚠️ Suspicious  
     - 🚫 Dangerous
   - Summary statistics show at the top

5. **Cancel if Needed:**
   - Click **"⛔ CANCEL"** to stop batch processing
   - Already processed results are saved

6. **Export Batch Results:**
   - Click **"📤 Export Batch Results"** when complete
   - Choose your preferred format (JSON/CSV/TXT)

7. **Return to Single Mode:**
   - Click **"🔗 Single Mode"** to go back

### Tips:
- URLs are processed one at a time to avoid rate limits
- Invalid URLs are skipped with an error message
- All results are automatically saved to history
- You can export results at any time

---

## 📤 Feature 2: Export Results

### Single URL Export:

1. **After Scanning:**
   - Complete a URL scan
   - Look for the **"📤 Export Result"** button below results

2. **Choose Format:**
   - Click the export button
   - Select your preferred format:
     - **📄 JSON** - Structured data with full details
     - **📊 CSV** - Spreadsheet-friendly format
     - **📝 TXT** - Human-readable report

3. **Save File:**
   - Choose where to save the file
   - Click "Save"
   - Get a confirmation message

### Batch Export:

1. **After Batch Scanning:**
   - Complete a batch scan
   - Click **"📤 Export Batch Results"**

2. **Choose Format:**
   - Same three formats available
   - Batch exports include summary statistics

3. **Save File:**
   - Choose location and save

### Export Formats Explained:

**JSON Format:**
- Contains all scan data
- Includes metadata and timestamps
- Best for: Data processing, archiving

**CSV Format:**
- Tabular format with columns
- Columns: URL, Status, Threat Types, Risk Score, Timestamp
- Best for: Excel, spreadsheets, data analysis

**TXT Format:**
- Human-readable report
- Organized in sections
- Includes recommendations
- Best for: Reading, sharing, documentation

---

## ✓ Feature 3: URL Validation and Formatting

### Real-Time Validation:

As you type a URL, you'll see validation feedback below the input field:

**Status Indicators:**
- ✓ **Valid URL** (green) - Good to go!
- ⚠️ **Warning** (yellow) - Suspicious pattern detected
- ✗ **Invalid** (red) - Fix the URL format
- 💡 **Suggestion** (blue) - Helpful tip

### Examples:

**Input:** `google.com`  
**Feedback:** ✓ Valid URL  
**Action:** Auto-formatted to `https://google.com`

**Input:** `192.168.1.1`  
**Feedback:** ⚠️ Warning: URL uses IP address instead of domain name  
**Action:** You can proceed but be cautious

**Input:** `gogle.com`  
**Feedback:** ⚠️ Possible typo  
**Suggestion:** 💡 Did you mean 'google.com'?

**Input:** `test.xyz/login`  
**Feedback:** ⚠️ Warning: Suspicious TLD, URL contains 'login'  
**Action:** Extra caution recommended

### Auto-Formatting:

URLs are automatically formatted when you analyze:
- Missing `https://` is added automatically
- HTTPS is preferred over HTTP
- Common patterns are recognized

### What Gets Flagged:

**Suspicious Patterns:**
- ⚠️ IP addresses (e.g., `192.168.1.1`)
- ⚠️ Suspicious TLDs (`.xyz`, `.tk`, `.ml`, etc.)
- ⚠️ Unusual ports (e.g., `:8888`)
- ⚠️ Phishing keywords (`login`, `verify`, `secure`, etc.)

**Common Typos Detected:**
- `gogle` → `google`
- `paypa1` → `paypal`
- `facbook` → `facebook`
- And more!

---

## 📅 Feature 4: Recent URLs Dropdown

### How to Use:

1. **Open Dropdown:**
   - Click the **"▼"** button next to the URL input field
   - Button changes to **"▲"** when open

2. **View Recent URLs:**
   - See your last 15 scanned URLs
   - Most recent appears at the top

3. **Select a URL:**
   - Click any URL in the list
   - It populates the input field automatically
   - Dropdown closes automatically

4. **Clear History:**
   - Right-click anywhere in the dropdown
   - Select "Clear History"
   - Confirm when prompted
   - All recent URLs are removed

### Tips:
- Recent URLs are saved between sessions
- URLs are automatically added when you scan
- Duplicate URLs show most recent scan
- Empty state shows "(No recent URLs)"

---

## 🎯 Quick Start Guide

### First Time Using New Features:

1. **Try URL Validation:**
   - Type `example.com` in the input field
   - Watch it validate in real-time
   - See it auto-format to `https://example.com`

2. **Test Export:**
   - Analyze a URL
   - Click **"📤 Export Result"**
   - Try exporting as TXT to see the formatted report

3. **Try Batch Mode:**
   - Click **"📊 Batch Mode"**
   - Enter 3-5 test URLs
   - Click **"📊 ANALYZE BATCH"**
   - Watch the progress
   - Export the results

4. **Use Recent URLs:**
   - After scanning a few URLs
   - Click the **"▼"** dropdown
   - Select a previous URL to re-scan

---

## 💡 Pro Tips

### Batch Scanning:
- ✅ Process up to 50 URLs at once efficiently
- ✅ Use the cancel button if you need to stop
- ✅ Export batch results for record-keeping
- ✅ Check the summary statistics before exporting

### Validation:
- ✅ Pay attention to warnings about suspicious patterns
- ✅ Use suggested corrections for typos
- ✅ IP addresses are unusual - verify the source
- ✅ Suspicious TLDs are often used in phishing

### Exporting:
- ✅ Use JSON for complete data preservation
- ✅ Use CSV for analysis in Excel/spreadsheets
- ✅ Use TXT for human-readable reports
- ✅ Export batch results to track multiple scans

### Recent URLs:
- ✅ Quick way to re-check URLs
- ✅ Clear history periodically for privacy
- ✅ Right-click for additional options
- ✅ Most recent URLs appear first

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Analyze current URL |
| `Ctrl+L` or `Escape` | Clear all and reset |
| Double-click history item | Re-analyze that URL |
| Right-click recent URLs | Show clear history option |

---

## 🆘 Troubleshooting

### Batch Mode Issues:

**Q: Batch processing seems slow**  
A: URLs are processed sequentially to respect API rate limits. This is by design for reliability.

**Q: One URL failed in my batch**  
A: The scanner continues with remaining URLs. Check the error message for the failed URL and try it separately.

**Q: Cancel button not working**  
A: The current URL will finish, then processing stops. This prevents data corruption.

### Export Issues:

**Q: Export button not showing**  
A: Make sure you've completed a scan first. The button only appears after results are available.

**Q: Can't choose save location**  
A: Check file permissions for your selected folder. Try saving to Documents or Desktop.

**Q: File format not what I expected**  
A: Each format has a different structure. Check the format descriptions in this guide.

### Validation Issues:

**Q: Why is my URL marked suspicious?**  
A: The validator flags potentially dangerous patterns (IP addresses, suspicious TLDs, etc.). You can still proceed if you trust the source.

**Q: Auto-format changed my URL**  
A: The validator adds `https://` for security. Your original URL is preserved in the input field.

**Q: Typo suggestion is wrong**  
A: Suggestions are based on common patterns. You can ignore them if your URL is correct.

### Recent URLs Issues:

**Q: Recent URLs not showing**  
A: Make sure you've scanned at least one URL. History persists between sessions.

**Q: Can't clear history**  
A: Right-click on the dropdown and select "Clear History". Confirm when prompted.

**Q: Too many URLs in dropdown**  
A: The list is automatically limited to 15 most recent URLs.

---

## 📞 Support

If you encounter any issues:

1. Check this user guide for solutions
2. Review the `IMPLEMENTATION_SUMMARY.md` for technical details
3. Check the console output for error messages
4. Report issues with specific examples

---

## 🎉 Enjoy the Enhanced Features!

These new features make Link Safety Checker more powerful and user-friendly:
- **Save time** with batch scanning
- **Keep records** with export functionality  
- **Stay safe** with enhanced validation
- **Work faster** with recent URLs access

**Happy scanning!** 🛡️

---

*For more information about the Link Safety Checker, see the main README.md file.*
