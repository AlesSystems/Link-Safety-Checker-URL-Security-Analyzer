"""Graphical User Interface for Link Safety Checker."""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api_client import check_url_safety, APIKeyError, RateLimitError, NetworkError, SafeBrowsingAPIError
from src.response_parser import parse_safe_browsing_response
from src.url_analyzer import analyze_url_complete


class LinkSafetyCheckerGUI:
    """Main GUI application for Link Safety Checker."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Link Safety Checker - AlesSystems")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        self.root.minsize(650, 500)
        
        # Modern gradient background colors
        self.bg_gradient_top = "#0f2027"
        self.bg_gradient_mid = "#203a43"
        self.bg_gradient_bottom = "#2c5364"
        
        # Set window background
        self.root.configure(bg=self.bg_gradient_mid)
        
        # Create main container with modern styling
        main_frame = tk.Frame(root, bg=self.bg_gradient_mid)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Animated header section with gradient effect
        header_frame = tk.Frame(main_frame, bg=self.bg_gradient_top, relief=tk.FLAT)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Large shield icon with modern styling
        icon_label = tk.Label(
            header_frame,
            text="🛡️",
            font=("Segoe UI Emoji", 60),
            bg=self.bg_gradient_top,
            fg="#00d4ff"
        )
        icon_label.pack(pady=(20, 10))
        
        # Modern title with gradient effect
        title_label = tk.Label(
            header_frame,
            text="Link Safety Checker",
            font=("Segoe UI", 32, "bold"),
            bg=self.bg_gradient_top,
            fg="#ffffff"
        )
        title_label.pack(pady=(0, 5))
        
        # Glowing subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="⚡ API + AI-Powered Rule-Based Analysis ⚡",
            font=("Segoe UI", 11),
            bg=self.bg_gradient_top,
            fg="#00d4ff"
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Organization branding
        brand_label = tk.Label(
            header_frame,
            text="Developed by AlesSystems",
            font=("Segoe UI", 9, "italic"),
            bg=self.bg_gradient_top,
            fg="#7f8c8d"
        )
        brand_label.pack(pady=(0, 20))
        
        # Card-style input container
        input_card = tk.Frame(
            main_frame,
            bg="#1a1a2e",
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground="#00d4ff",
            highlightcolor="#00d4ff"
        )
        input_card.pack(fill=tk.X, pady=(0, 20))
        
        # URL label with icon
        url_label_frame = tk.Frame(input_card, bg="#1a1a2e")
        url_label_frame.pack(fill=tk.X, padx=25, pady=(20, 10))
        
        url_icon = tk.Label(
            url_label_frame,
            text="🔗",
            font=("Segoe UI Emoji", 14),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        url_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        url_label = tk.Label(
            url_label_frame,
            text="Enter URL to analyze:",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        )
        url_label.pack(side=tk.LEFT)
        
        # Modern entry field with custom styling
        entry_frame = tk.Frame(input_card, bg="#1a1a2e")
        entry_frame.pack(fill=tk.X, padx=25, pady=(0, 25))
        
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(
            entry_frame,
            textvariable=self.url_var,
            font=("Segoe UI", 13),
            bg="#2d2d44",
            fg="#ffffff",
            insertbackground="#00d4ff",
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground="#00d4ff",
            highlightcolor="#00ff88"
        )
        self.url_entry.pack(fill=tk.X, ipady=12, ipadx=10)
        self.url_entry.focus()
        
        # Bind Enter key to analyze
        self.url_entry.bind('<Return>', lambda e: self.analyze_url())
        self.url_entry.bind('<FocusIn>', self.on_entry_focus)
        self.url_entry.bind('<FocusOut>', self.on_entry_unfocus)
        
        # Modern gradient button with hover effect
        button_frame = tk.Frame(main_frame, bg=self.bg_gradient_mid)
        button_frame.pack(pady=(0, 20))
        
        self.analyze_button = tk.Button(
            button_frame,
            text="🔍  ANALYZE LINK",
            command=self.analyze_url,
            font=("Segoe UI", 14, "bold"),
            bg="#00d4ff",
            fg="#0f2027",
            activebackground="#00ff88",
            activeforeground="#0f2027",
            cursor="hand2",
            relief=tk.FLAT,
            padx=40,
            pady=15,
            borderwidth=0
        )
        self.analyze_button.pack()
        
        # Add hover effects
        self.analyze_button.bind('<Enter>', self.on_button_hover)
        self.analyze_button.bind('<Leave>', self.on_button_leave)
        
        # Result card with modern styling
        self.result_card = tk.Frame(
            main_frame,
            bg="#1a1a2e",
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground="#2d2d44"
        )
        self.result_card.pack(fill=tk.BOTH, expand=True)
        
        # Result icon (hidden by default)
        self.result_icon = tk.Label(
            self.result_card,
            text="",
            font=("Segoe UI Emoji", 48),
            bg="#1a1a2e"
        )
        self.result_icon.pack(pady=(20, 10))
        
        # Result label
        self.result_label = tk.Label(
            self.result_card,
            text="",
            font=("Segoe UI", 18, "bold"),
            bg="#1a1a2e",
            wraplength=600,
            justify=tk.CENTER
        )
        self.result_label.pack(pady=(0, 10))
        
        # Details label
        self.details_label = tk.Label(
            self.result_card,
            text="",
            font=("Segoe UI", 11),
            bg="#1a1a2e",
            wraplength=600,
            justify=tk.CENTER,
            fg="#b8b8d1"
        )
        self.details_label.pack(pady=(0, 20))
        
        # Modern status bar
        self.status_label = tk.Label(
            root,
            text="● Ready",
            font=("Segoe UI", 10),
            fg="#00d4ff",
            bg="#0f2027",
            anchor=tk.W,
            padx=20,
            pady=8
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_entry_focus(self, event):
        """Handle entry field focus."""
        self.url_entry.config(highlightbackground="#00ff88")
    
    def on_entry_unfocus(self, event):
        """Handle entry field unfocus."""
        self.url_entry.config(highlightbackground="#00d4ff")
    
    def on_button_hover(self, event):
        """Handle button hover effect."""
        self.analyze_button.config(bg="#00ff88", fg="#0f2027")
    
    def on_button_leave(self, event):
        """Handle button leave effect."""
        self.analyze_button.config(bg="#00d4ff", fg="#0f2027")
    
    def validate_input(self):
        """Validate the URL input field."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning(
                "Input Required",
                "Please enter a URL to analyze."
            )
            return False
        return True
    
    def set_status(self, message, color="#00d4ff"):
        """Update status bar message."""
        self.status_label.config(text=f"● {message}", fg=color)
    
    def disable_button(self):
        """Disable analyze button during processing."""
        self.analyze_button.config(state=tk.DISABLED, bg="#555577", cursor="wait")
        self.url_entry.config(state=tk.DISABLED)
    
    def enable_button(self):
        """Enable analyze button after processing."""
        self.analyze_button.config(state=tk.NORMAL, bg="#00d4ff", cursor="hand2")
        self.url_entry.config(state=tk.NORMAL)
    
    def clear_results(self):
        """Clear previous results."""
        self.result_icon.config(text="")
        self.result_label.config(text="", fg="#ffffff")
        self.details_label.config(text="", fg="#b8b8d1")
        self.result_card.config(highlightbackground="#2d2d44")
    
    def display_result(self, verdict):
        """Display the safety check result with modern styling and rule-based analysis."""
        status = verdict.verdict if hasattr(verdict, 'verdict') else verdict.status
        rule_score = verdict.rule_based_score.get('total_score', 0) if hasattr(verdict, 'rule_based_score') else 0
        
        if status == "safe":
            self.result_icon.config(text="✅", fg="#00ff88")
            self.result_label.config(
                text="SAFE TO VISIT",
                fg="#00ff88"
            )
            details = "✓ No threats detected\n✓ Verified by multiple security checks\n✓ This link appears to be legitimate and safe"
            if hasattr(verdict, 'rule_based_score'):
                details += f"\n📊 Risk Score: {rule_score}/100"
            self.details_label.config(text=details, fg="#00ff88")
            self.result_card.config(highlightbackground="#00ff88")
            
        elif status == "suspicious":
            self.result_icon.config(text="⚠️", fg="#ffd700")
            self.result_label.config(
                text="POTENTIALLY SUSPICIOUS",
                fg="#ffd700"
            )
            details_parts = []
            if hasattr(verdict, 'reasons') and verdict.reasons:
                details_parts.append(f"⚠ {verdict.reasons[0]}")
            else:
                threat_types = verdict.api_data.get('threat_types', []) if hasattr(verdict, 'api_data') else verdict.threat_types
                if threat_types:
                    details_parts.append(f"⚠ Detected: {', '.join(threat_types)}")
            details_parts.append("⚠ Proceed with extreme caution")
            details_parts.append("⚠ Consider avoiding this link")
            if hasattr(verdict, 'rule_based_score'):
                details_parts.append(f"📊 Risk Score: {rule_score}/100")
            self.details_label.config(text="\n".join(details_parts), fg="#ffd700")
            self.result_card.config(highlightbackground="#ffd700")
            
        elif status == "dangerous":
            self.result_icon.config(text="🚫", fg="#ff3366")
            self.result_label.config(
                text="⚠️ DANGEROUS - DO NOT VISIT ⚠️",
                fg="#ff3366"
            )
            details_parts = []
            if hasattr(verdict, 'reasons') and verdict.reasons:
                details_parts.append(f"🚨 {verdict.reasons[0]}")
            else:
                threat_types = verdict.api_data.get('threat_types', []) if hasattr(verdict, 'api_data') else verdict.threat_types
                if threat_types:
                    details_parts.append(f"🚨 Threats: {', '.join(threat_types)}")
            details_parts.append("🚨 This site may harm your computer")
            details_parts.append("🚨 DO NOT click or visit this link!")
            if hasattr(verdict, 'rule_based_score'):
                details_parts.append(f"📊 Risk Score: {rule_score}/100")
            self.details_label.config(text="\n".join(details_parts), fg="#ff3366")
            self.result_card.config(highlightbackground="#ff3366")
    
    def display_error(self, error_message):
        """Display error message with modern styling."""
        self.result_icon.config(text="❌", fg="#ff6b6b")
        self.result_label.config(
            text="ERROR",
            fg="#ff6b6b"
        )
        self.details_label.config(
            text=error_message,
            fg="#ff6b6b"
        )
        self.result_card.config(highlightbackground="#ff6b6b")
    
    def analyze_url_thread(self, url):
        """Perform URL analysis in background thread."""
        try:
            # Perform complete analysis (API + rules)
            self.root.after(0, lambda: self.set_status(f"Analyzing URL...", "#ffd700"))
            verdict = analyze_url_complete(url)
            
            # Update UI on main thread
            self.root.after(0, lambda: self.display_result(verdict))
            status_colors = {"safe": "#00ff88", "suspicious": "#ffd700", "dangerous": "#ff3366"}
            status_text = {"safe": "Verification complete - Safe", "suspicious": "Verification complete - Suspicious", "dangerous": "Verification complete - Dangerous"}
            self.root.after(0, lambda: self.set_status(status_text[verdict.verdict], status_colors[verdict.verdict]))
            
        except APIKeyError as e:
            error_msg = "⚠️ API Key Error\n\nPlease configure your Google Safe Browsing API key in the .env file.\nGet your free API key from Google Cloud Console."
            self.root.after(0, lambda: self.display_error(error_msg))
            self.root.after(0, lambda: self.set_status("API key not configured", "#ff6b6b"))
            
        except RateLimitError as e:
            error_msg = "⏳ Rate Limit Exceeded\n\nToo many requests. Please wait a few minutes and try again."
            self.root.after(0, lambda: self.display_error(error_msg))
            self.root.after(0, lambda: self.set_status("Rate limit exceeded", "#ff6b6b"))
            
        except NetworkError as e:
            error_msg = "🌐 Connection Error\n\nCannot reach Google Safe Browsing API.\nPlease check your internet connection and try again."
            self.root.after(0, lambda: self.display_error(error_msg))
            self.root.after(0, lambda: self.set_status("Network connection failed", "#ff6b6b"))
            
        except SafeBrowsingAPIError as e:
            error_msg = "⚠️ Service Error\n\nUnable to complete the security check.\nPlease try again in a few moments."
            self.root.after(0, lambda: self.display_error(error_msg))
            self.root.after(0, lambda: self.set_status("API request failed", "#ff6b6b"))
            
        except Exception as e:
            error_msg = f"⚠️ Unexpected Error\n\n{str(e)}\n\nPlease try again or contact support if the issue persists."
            self.root.after(0, lambda: self.display_error(error_msg))
            self.root.after(0, lambda: self.set_status("Unexpected error occurred", "#ff6b6b"))
        
        finally:
            self.root.after(0, self.enable_button)
    
    def analyze_url(self):
        """Handle analyze button click."""
        # Validate input
        if not self.validate_input():
            return
        
        # Get URL
        url = self.url_var.get().strip()
        
        # Clear previous results
        self.clear_results()
        
        # Disable button during processing
        self.disable_button()
        self.set_status("Initializing security scan...", "#ffd700")
        
        # Run analysis in background thread to prevent UI freezing
        thread = threading.Thread(target=self.analyze_url_thread, args=(url,), daemon=True)
        thread.start()


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = LinkSafetyCheckerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
