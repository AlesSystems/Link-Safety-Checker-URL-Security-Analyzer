"""Graphical User Interface for Link Safety Checker."""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api_client import check_url_safety, APIKeyError, RateLimitError, NetworkError, SafeBrowsingAPIError
from src.response_parser import parse_safe_browsing_response
from src.url_analyzer import analyze_url_complete
from src.gui_history import ScanHistory

# Try to import pyperclip, fallback to tkinter clipboard if not available
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


class LinkSafetyCheckerGUI:
    """Main GUI application for Link Safety Checker."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Link Safety Checker - AlesSystems")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        self.root.minsize(850, 600)
        
        # Initialize history manager
        self.history = ScanHistory()
        self.current_result = None  # Store current result for copying
        
        # Modern gradient background colors
        self.bg_gradient_top = "#0f2027"
        self.bg_gradient_mid = "#203a43"
        self.bg_gradient_bottom = "#2c5364"
        
        # Set window background
        self.root.configure(bg=self.bg_gradient_mid)
        
        # Create main container with modern styling
        main_container = tk.Frame(root, bg=self.bg_gradient_mid)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel (main content)
        main_frame = tk.Frame(main_container, bg=self.bg_gradient_mid)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel (history sidebar)
        history_frame = tk.Frame(main_container, bg="#1a1a2e", width=250, relief=tk.FLAT,
                                highlightthickness=2, highlightbackground="#2d2d44")
        history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        history_frame.pack_propagate(False)
        
        # History header
        history_header = tk.Label(
            history_frame,
            text="📜 Scan History",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        history_header.pack(pady=(15, 10), padx=10)
        
        # History listbox with scrollbar
        history_scroll_frame = tk.Frame(history_frame, bg="#1a1a2e")
        history_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        history_scrollbar = tk.Scrollbar(history_scroll_frame)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(
            history_scroll_frame,
            font=("Segoe UI", 9),
            bg="#2d2d44",
            fg="#ffffff",
            selectbackground="#00d4ff",
            selectforeground="#0f2027",
            relief=tk.FLAT,
            highlightthickness=0,
            yscrollcommand=history_scrollbar.set
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.config(command=self.history_listbox.yview)
        
        # Bind double-click to re-analyze
        self.history_listbox.bind('<Double-Button-1>', self.on_history_select)
        
        # Load initial history
        self.refresh_history()
        
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
        entry_frame.pack(fill=tk.X, padx=25, pady=(0, 10))
        
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
        
        # Button row (Copy URL and Clear buttons)
        button_row = tk.Frame(input_card, bg="#1a1a2e")
        button_row.pack(fill=tk.X, padx=25, pady=(0, 20))
        
        self.copy_url_button = tk.Button(
            button_row,
            text="📋 Copy URL",
            command=self.copy_url_to_clipboard,
            font=("Segoe UI", 10),
            bg="#2d2d44",
            fg="#00d4ff",
            activebackground="#00d4ff",
            activeforeground="#1a1a2e",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            borderwidth=0
        )
        self.copy_url_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = tk.Button(
            button_row,
            text="🗑️ Clear",
            command=self.clear_all,
            font=("Segoe UI", 10),
            bg="#2d2d44",
            fg="#ff6b6b",
            activebackground="#ff6b6b",
            activeforeground="#1a1a2e",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            borderwidth=0
        )
        self.clear_button.pack(side=tk.LEFT)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-l>', lambda e: self.clear_all())
        self.root.bind('<Escape>', lambda e: self.clear_all())
        
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
        self.details_label.pack(pady=(0, 15))
        
        # Timestamp label (Feature 5)
        self.timestamp_label = tk.Label(
            self.result_card,
            text="",
            font=("Segoe UI", 9, "italic"),
            bg="#1a1a2e",
            fg="#7f8c8d"
        )
        # Don't pack initially, will be shown after scan
        
        # View Details button (Feature 4)
        self.view_details_button = tk.Button(
            self.result_card,
            text="📋 View Details",
            command=self.toggle_threat_details,
            font=("Segoe UI", 10),
            bg="#2d2d44",
            fg="#00d4ff",
            activebackground="#00d4ff",
            activeforeground="#1a1a2e",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            borderwidth=0
        )
        # Don't pack initially, will be shown after scan
        
        # Threat details frame (Feature 4) - expandable section
        self.threat_details_frame = tk.Frame(
            self.result_card,
            bg="#1a1a2e"
        )
        self.threat_details_visible = False
        
        # Threat details text widget with scrollbar
        details_scroll_frame = tk.Frame(self.threat_details_frame, bg="#1a1a2e")
        details_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        details_scrollbar = tk.Scrollbar(details_scroll_frame)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.threat_details_text = tk.Text(
            details_scroll_frame,
            font=("Consolas", 10),
            bg="#2d2d44",
            fg="#ffffff",
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=12,
            yscrollcommand=details_scrollbar.set,
            state=tk.DISABLED
        )
        self.threat_details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_scrollbar.config(command=self.threat_details_text.yview)
        
        # Copy Result button (initially hidden)
        self.copy_result_button = tk.Button(
            self.result_card,
            text="📋 Copy Result",
            command=self.copy_result_to_clipboard,
            font=("Segoe UI", 10),
            bg="#2d2d44",
            fg="#00d4ff",
            activebackground="#00d4ff",
            activeforeground="#1a1a2e",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            borderwidth=0
        )
        # Don't pack initially, will be shown after scan
        
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
        self.copy_result_button.pack_forget()  # Hide copy result button
        self.timestamp_label.pack_forget()  # Hide timestamp
        self.view_details_button.pack_forget()  # Hide view details button
        self.threat_details_frame.pack_forget()  # Hide threat details
        self.threat_details_visible = False
        self.current_result = None
    
    def clear_all(self):
        """Clear all input and results, reset UI to initial state."""
        self.url_var.set("")
        self.clear_results()
        self.set_status("Ready", "#00d4ff")
        self.url_entry.focus()
    
    def refresh_history(self):
        """Refresh the history listbox with recent scans."""
        self.history_listbox.delete(0, tk.END)
        recent_scans = self.history.get_recent_scans(50)
        
        for scan in recent_scans:
            # Format: status icon + truncated URL
            status_icons = {"safe": "✅", "suspicious": "⚠️", "dangerous": "🚫"}
            icon = status_icons.get(scan['status'], "❓")
            url = scan['url']
            # Truncate URL if too long
            if len(url) > 35:
                url = url[:32] + "..."
            
            # Parse timestamp for display
            try:
                dt = datetime.fromisoformat(scan['timestamp'])
                time_str = dt.strftime("%m/%d %H:%M")
            except:
                time_str = "Unknown"
            
            display_text = f"{icon} {url}\n   {time_str}"
            self.history_listbox.insert(tk.END, display_text)
    
    def on_history_select(self, event):
        """Handle double-click on history item to re-analyze URL."""
        selection = self.history_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        scans = self.history.get_recent_scans(50)
        
        if index < len(scans):
            url = scans[index]['url']
            self.url_var.set(url)
            self.analyze_url()
    
    def copy_url_to_clipboard(self):
        """Copy the current URL to clipboard."""
        url = self.url_var.get().strip()
        if not url:
            self.set_status("No URL to copy", "#ff6b6b")
            return
        
        try:
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(url)
            else:
                self.root.clipboard_clear()
                self.root.clipboard_append(url)
                self.root.update()
            
            self.set_status("✓ URL copied to clipboard", "#00ff88")
        except Exception as e:
            self.set_status(f"Failed to copy URL: {str(e)}", "#ff6b6b")
    
    def copy_result_to_clipboard(self):
        """Copy the formatted scan result to clipboard."""
        if not self.current_result:
            self.set_status("No result to copy", "#ff6b6b")
            return
        
        try:
            # Format result text
            url = self.url_var.get().strip()
            status = self.current_result['status'].upper()
            threats = ", ".join(self.current_result['threats']) if self.current_result['threats'] else "None"
            timestamp = self.current_result['timestamp']
            
            result_text = f"""Link Safety Checker - Scan Result
Status: {status}
URL: {url}
Threats: {threats}
Scanned: {timestamp}"""
            
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(result_text)
            else:
                self.root.clipboard_clear()
                self.root.clipboard_append(result_text)
                self.root.update()
            
            self.set_status("✓ Result copied to clipboard", "#00ff88")
        except Exception as e:
            self.set_status(f"Failed to copy result: {str(e)}", "#ff6b6b")
    
    def format_timestamp(self, timestamp_str: str) -> str:
        """Format timestamp for display (Feature 5).
        
        Args:
            timestamp_str: ISO format timestamp string
            
        Returns:
            Formatted timestamp string like "Jan 15, 2024 at 10:30 AM"
        """
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%b %d, %Y at %I:%M %p")
        except:
            return timestamp_str
    
    def format_relative_time(self, timestamp_str: str) -> str:
        """Format timestamp as relative time (Feature 5).
        
        Args:
            timestamp_str: ISO format timestamp string
            
        Returns:
            Relative time string like "2 minutes ago" or absolute for old scans
        """
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
            diff = now - dt
            
            seconds = diff.total_seconds()
            
            if seconds < 60:
                return "Just now"
            elif seconds < 3600:
                minutes = int(seconds / 60)
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            elif seconds < 86400:
                hours = int(seconds / 3600)
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif seconds < 604800:  # Less than a week
                days = int(seconds / 86400)
                return f"{days} day{'s' if days != 1 else ''} ago"
            else:
                # After 1 week, switch to absolute format
                return dt.strftime("%b %d, %Y at %I:%M %p")
        except:
            return timestamp_str
    
    def toggle_threat_details(self):
        """Toggle the visibility of threat details section (Feature 4)."""
        if self.threat_details_visible:
            # Hide details
            self.threat_details_frame.pack_forget()
            self.view_details_button.config(text="📋 View Details")
            self.threat_details_visible = False
        else:
            # Show details
            self.threat_details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            self.view_details_button.config(text="📋 Hide Details")
            self.threat_details_visible = True
    
    def display_threat_details(self, verdict):
        """Display detailed threat information in tree structure (Feature 4).
        
        Args:
            verdict: The FinalSecurityVerdict object with analysis details
        """
        self.threat_details_text.config(state=tk.NORMAL)
        self.threat_details_text.delete(1.0, tk.END)
        
        details_lines = []
        details_lines.append("=" * 60)
        details_lines.append("DETAILED THREAT ANALYSIS")
        details_lines.append("=" * 60)
        details_lines.append("")
        
        # API Data Section
        details_lines.append("🌐 API Analysis (Google Safe Browsing)")
        details_lines.append("─" * 60)
        
        if hasattr(verdict, 'api_data') and verdict.api_data:
            api_available = verdict.api_data.get('available', False)
            details_lines.append(f"├─ API Status: {'Available ✓' if api_available else 'Unavailable ✗'}")
            
            threat_types = verdict.api_data.get('threat_types', [])
            if threat_types:
                details_lines.append(f"├─ Threat Types Detected: {len(threat_types)}")
                for i, threat in enumerate(threat_types):
                    prefix = "├─" if i < len(threat_types) - 1 else "└─"
                    details_lines.append(f"│  {prefix} {threat}")
            else:
                details_lines.append("└─ No threats detected")
            
            # Raw API matches if available
            if 'raw_response' in verdict.api_data and verdict.api_data['raw_response']:
                raw_resp = verdict.api_data['raw_response']
                matches = raw_resp.get('matches', [])
                if matches:
                    details_lines.append("")
                    details_lines.append("📊 Match Details:")
                    for i, match in enumerate(matches):
                        details_lines.append(f"│")
                        details_lines.append(f"├─ Match #{i+1}")
                        details_lines.append(f"│  ├─ Threat Type: {match.get('threatType', 'Unknown')}")
                        details_lines.append(f"│  ├─ Platform: {match.get('platformType', 'Unknown')}")
                        details_lines.append(f"│  ├─ Threat Entry: {match.get('threatEntryType', 'Unknown')}")
                        cache_duration = match.get('cacheDuration', 'Unknown')
                        details_lines.append(f"│  └─ Cache Duration: {cache_duration}")
        else:
            details_lines.append("└─ No API data available")
        
        details_lines.append("")
        
        # Rule-Based Analysis Section
        details_lines.append("🤖 Rule-Based Analysis (AI-Powered)")
        details_lines.append("─" * 60)
        
        if hasattr(verdict, 'rule_based_score') and verdict.rule_based_score:
            score_data = verdict.rule_based_score
            total_score = score_data.get('total_score', 0)
            details_lines.append(f"├─ Total Risk Score: {total_score}/100")
            
            # Individual component scores
            if 'components' in score_data:
                components = score_data['components']
                details_lines.append("├─ Score Components:")
                for key, value in components.items():
                    details_lines.append(f"│  ├─ {key.replace('_', ' ').title()}: {value}")
            
            # Risk factors
            if 'risk_factors' in score_data:
                risk_factors = score_data['risk_factors']
                if risk_factors:
                    details_lines.append("├─ Risk Factors Detected:")
                    for i, factor in enumerate(risk_factors):
                        prefix = "└─" if i == len(risk_factors) - 1 else "├─"
                        details_lines.append(f"│  {prefix} {factor}")
                else:
                    details_lines.append("└─ No significant risk factors")
        else:
            details_lines.append("└─ No rule-based analysis available")
        
        details_lines.append("")
        
        # Final Verdict Section
        details_lines.append("⚖️  Final Verdict")
        details_lines.append("─" * 60)
        details_lines.append(f"├─ Classification: {verdict.verdict.upper()}")
        
        if hasattr(verdict, 'reasons') and verdict.reasons:
            details_lines.append("└─ Reasoning:")
            for i, reason in enumerate(verdict.reasons):
                prefix = "   └─" if i == len(verdict.reasons) - 1 else "   ├─"
                details_lines.append(f"{prefix} {reason}")
        
        details_lines.append("")
        details_lines.append("=" * 60)
        
        # Insert all lines
        self.threat_details_text.insert(1.0, "\n".join(details_lines))
        self.threat_details_text.config(state=tk.DISABLED)
    
    
    def display_result(self, verdict):
        """Display the safety check result with modern styling and rule-based analysis."""
        status = verdict.verdict if hasattr(verdict, 'verdict') else verdict.status
        rule_score = verdict.rule_based_score.get('total_score', 0) if hasattr(verdict, 'rule_based_score') else 0
        
        # Extract threat types for storage
        threat_types = []
        if hasattr(verdict, 'api_data') and 'threat_types' in verdict.api_data:
            threat_types = verdict.api_data.get('threat_types', [])
        elif hasattr(verdict, 'threat_types'):
            threat_types = verdict.threat_types
        
        # Store current result for copying (Feature 5 - include timestamp)
        timestamp_str = datetime.now().strftime("%b %d, %Y at %I:%M %p")
        self.current_result = {
            'status': status,
            'threats': threat_types,
            'timestamp': timestamp_str,
            'verdict': verdict  # Store full verdict for details view
        }
        
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
                if threat_types:
                    details_parts.append(f"🚨 Threats: {', '.join(threat_types)}")
            details_parts.append("🚨 This site may harm your computer")
            details_parts.append("🚨 DO NOT click or visit this link!")
            if hasattr(verdict, 'rule_based_score'):
                details_parts.append(f"📊 Risk Score: {rule_score}/100")
            self.details_label.config(text="\n".join(details_parts), fg="#ff3366")
            self.result_card.config(highlightbackground="#ff3366")
        
        # Feature 5: Display timestamp with relative time
        timestamp_display = f"📅 Scanned: {timestamp_str}"
        if hasattr(verdict, 'timestamp'):
            relative_time = self.format_relative_time(verdict.timestamp)
            timestamp_display += f" ({relative_time})"
        self.timestamp_label.config(text=timestamp_display)
        self.timestamp_label.pack(pady=(0, 10))
        
        # Feature 4: Populate threat details
        self.display_threat_details(verdict)
        
        # Show view details button
        self.view_details_button.pack(pady=(0, 10))
        
        # Show copy result button
        self.copy_result_button.pack(pady=(0, 20))
    
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
            
            # Save to history
            self.history.save_scan_to_history(url, verdict)
            
            # Update UI on main thread
            self.root.after(0, lambda: self.display_result(verdict))
            self.root.after(0, self.refresh_history)
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
