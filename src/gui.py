"""Graphical User Interface for Link Safety Checker."""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
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
from src.gui_export import ExportManager
from src.url_validator import URLValidator, URLValidationResult

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
        # Get screen dimensions for responsive sizing
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Use 80% of screen size, with reasonable defaults
        window_width = max(900, int(screen_width * 0.8))
        window_height = max(650, int(screen_height * 0.75))
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(True, True)
        self.root.minsize(800, 550)
        
        # Initialize history manager
        self.history = ScanHistory()
        self.current_result = None  # Store current result for copying
        
        # Batch mode variables
        self.batch_mode = False
        self.batch_results = []
        self.batch_processing = False
        self.cancel_batch = False
        
        # Recent URLs (for dropdown - Feature 9)
        self.recent_urls = []
        self.recent_urls_dropdown_visible = False
        
        # URL validation
        self.validator = URLValidator()
        self.validation_result = None
        
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
        # Store main_frame reference for dynamic sizing
        self.main_frame = main_frame
        
        # Right panel (history sidebar)
        history_frame = tk.Frame(main_container, bg="#1a1a2e", width=250, relief=tk.FLAT,
                                highlightthickness=2, highlightbackground="#2d2d44")
        history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        history_frame.pack_propagate(False)
        
        # History header with clear button
        history_header_frame = tk.Frame(history_frame, bg="#1a1a2e")
        history_header_frame.pack(fill=tk.X, pady=(15, 8), padx=10)
        
        history_header = tk.Label(
            history_header_frame,
            text="📜 Scan History",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        history_header.pack(side=tk.LEFT)
        
        # Clear history button
        self.clear_history_button = tk.Button(
            history_header_frame,
            text="🗑️",
            command=self.clear_scan_history,
            font=("Segoe UI", 10),
            bg="#2d2d44",
            fg="#ff6b6b",
            activebackground="#ff6b6b",
            activeforeground="#1a1a2e",
            cursor="hand2",
            relief=tk.FLAT,
            padx=8,
            pady=4,
            borderwidth=0,
            anchor=tk.CENTER,
            justify=tk.CENTER
        )
        self.clear_history_button.pack(side=tk.RIGHT)
        
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
        
        # Compact header section with gradient effect
        header_frame = tk.Frame(main_frame, bg=self.bg_gradient_top, relief=tk.FLAT)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Shield icon - centered
        icon_label = tk.Label(
            header_frame,
            text="🛡️",
            font=("Segoe UI Emoji", 28),
            bg=self.bg_gradient_top,
            fg="#00d4ff"
        )
        icon_label.pack(anchor=tk.CENTER, pady=(10, 5))
        
        # Title and subtitle in vertical stack - centered
        title_stack = tk.Frame(header_frame, bg=self.bg_gradient_top)
        title_stack.pack(anchor=tk.CENTER, pady=(0, 5))
        
        # Modern title with gradient effect - smaller font
        title_label = tk.Label(
            title_stack,
            text="Link Safety Checker",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg_gradient_top,
            fg="#ffffff"
        )
        title_label.pack(anchor=tk.CENTER)
        
        # Glowing subtitle - smaller
        subtitle_label = tk.Label(
            title_stack,
            text="⚡ API + AI-Powered Rule-Based Analysis ⚡",
            font=("Segoe UI", 9),
            bg=self.bg_gradient_top,
            fg="#00d4ff"
        )
        subtitle_label.pack(anchor=tk.CENTER)
        
        # Organization branding - smaller and centered below subtitle
        brand_label = tk.Label(
            header_frame,
            text="Developed by AlesSystems",
            font=("Segoe UI", 8, "italic"),
            bg=self.bg_gradient_top,
            fg="#7f8c8d"
        )
        brand_label.pack(anchor=tk.CENTER, pady=(0, 5))
        
        # Card-style input container - more compact
        input_card = tk.Frame(
            main_frame,
            bg="#1a1a2e",
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground="#00d4ff",
            highlightcolor="#00d4ff"
        )
        input_card.pack(fill=tk.X, pady=(0, 12))
        
        # URL label with icon - more compact
        url_label_frame = tk.Frame(input_card, bg="#1a1a2e")
        url_label_frame.pack(fill=tk.X, padx=20, pady=(12, 8))
        
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
        entry_frame.pack(fill=tk.X, padx=20, pady=(0, 8))
        
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
        # Feature 8: Real-time URL validation
        self.url_var.trace('w', self.on_url_change)
        
        # Load recent URLs from history
        self.load_recent_urls()
        
        # Button row (Copy URL and Clear buttons) - more compact
        button_row = tk.Frame(input_card, bg="#1a1a2e")
        button_row.pack(fill=tk.X, padx=20, pady=(0, 12))
        
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
        
        # Mode toggle button (Feature 6 - Batch mode)
        self.mode_toggle_button = tk.Button(
            button_row,
            text="📊 Batch Mode",
            command=self.toggle_batch_mode,
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
        self.mode_toggle_button.pack(side=tk.RIGHT)
        
        # URL validation indicator (Feature 8)
        self.validation_indicator = tk.Label(
            input_card,
            text="",
            font=("Segoe UI", 9),
            bg="#1a1a2e",
            fg="#b8b8d1"
        )
        self.validation_indicator.pack(fill=tk.X, padx=20, pady=(0, 8))
        
        # Batch input frame (Feature 6) - hidden by default
        self.batch_input_frame = tk.Frame(input_card, bg="#1a1a2e")
        
        batch_label = tk.Label(
            self.batch_input_frame,
            text="📋 Enter URLs (one per line):",
            font=("Segoe UI", 11, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        batch_label.pack(pady=(10, 5), padx=25, anchor=tk.W)
        
        # Scrolled text for batch input
        batch_text_frame = tk.Frame(self.batch_input_frame, bg="#1a1a2e")
        batch_text_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 10))
        
        self.batch_text = scrolledtext.ScrolledText(
            batch_text_frame,
            font=("Segoe UI", 10),
            bg="#2d2d44",
            fg="#ffffff",
            insertbackground="#00d4ff",
            relief=tk.FLAT,
            height=8,
            wrap=tk.WORD
        )
        self.batch_text.pack(fill=tk.BOTH, expand=True)
        
        # Recent URLs dropdown button (Feature 9)
        self.recent_urls_button = tk.Button(
            entry_frame,
            text="▼",
            command=self.toggle_recent_urls_dropdown,
            font=("Segoe UI", 8),
            bg="#2d2d44",
            fg="#00d4ff",
            activebackground="#00d4ff",
            activeforeground="#1a1a2e",
            cursor="hand2",
            relief=tk.FLAT,
            width=2
        )
        self.recent_urls_button.place(relx=0.98, rely=0.5, anchor=tk.E)
        
        # Recent URLs dropdown listbox (Feature 9) - hidden by default
        self.recent_urls_listbox_frame = tk.Frame(
            input_card,
            bg="#2d2d44",
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#00d4ff"
        )
        
        recent_scroll = tk.Scrollbar(self.recent_urls_listbox_frame)
        recent_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.recent_urls_listbox = tk.Listbox(
            self.recent_urls_listbox_frame,
            font=("Segoe UI", 9),
            bg="#2d2d44",
            fg="#ffffff",
            selectbackground="#00d4ff",
            selectforeground="#1a1a2e",
            relief=tk.FLAT,
            height=6,
            yscrollcommand=recent_scroll.set
        )
        self.recent_urls_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        recent_scroll.config(command=self.recent_urls_listbox.yview)
        
        self.recent_urls_listbox.bind('<<ListboxSelect>>', self.on_recent_url_select)
        
        # Clear history option in recent URLs
        self.recent_urls_listbox.bind('<Button-3>', self.show_recent_urls_context_menu)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-l>', lambda e: self.clear_all())
        self.root.bind('<Escape>', lambda e: self.clear_all())
        
        # Modern gradient button with hover effect - more compact
        button_frame = tk.Frame(main_frame, bg=self.bg_gradient_mid)
        button_frame.pack(pady=(0, 12))
        
        self.analyze_button = tk.Button(
            button_frame,
            text="🔍  ANALYZE LINK",
            command=self.analyze_url,
            font=("Segoe UI", 12, "bold"),
            bg="#00d4ff",
            fg="#0f2027",
            activebackground="#00ff88",
            activeforeground="#0f2027",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            borderwidth=0
        )
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        # Batch analyze button (Feature 6) - hidden by default
        self.batch_analyze_button = tk.Button(
            button_frame,
            text="📊  ANALYZE BATCH",
            command=self.analyze_batch,
            font=("Segoe UI", 12, "bold"),
            bg="#00d4ff",
            fg="#0f2027",
            activebackground="#00ff88",
            activeforeground="#0f2027",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10,
            borderwidth=0
        )
        
        # Cancel batch button (Feature 6) - hidden by default
        self.cancel_batch_button = tk.Button(
            button_frame,
            text="⛔ CANCEL",
            command=self.cancel_batch_processing,
            font=("Segoe UI", 11, "bold"),
            bg="#ff6b6b",
            fg="#ffffff",
            activebackground="#ff3366",
            activeforeground="#ffffff",
            cursor="hand2",
            relief=tk.FLAT,
            padx=25,
            pady=10,
            borderwidth=0
        )
        
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
        
        # Result icon (hidden by default) - smaller
        self.result_icon = tk.Label(
            self.result_card,
            text="",
            font=("Segoe UI Emoji", 36),
            bg="#1a1a2e"
        )
        self.result_icon.pack(pady=(12, 8))
        
        # Result label - dynamic wraplength
        self.result_label = tk.Label(
            self.result_card,
            text="",
            font=("Segoe UI", 16, "bold"),
            bg="#1a1a2e",
            wraplength=500,
            justify=tk.CENTER
        )
        self.result_label.pack(pady=(0, 8))
        
        # Details label - dynamic wraplength
        self.details_label = tk.Label(
            self.result_card,
            text="",
            font=("Segoe UI", 10),
            bg="#1a1a2e",
            wraplength=500,
            justify=tk.CENTER,
            fg="#b8b8d1"
        )
        self.details_label.pack(pady=(0, 10))
        
        # Bind window resize to update wraplength dynamically
        def update_wraplength(event=None):
            try:
                # Get actual main_frame width
                main_frame_width = self.main_frame.winfo_width()
                if main_frame_width > 1:  # Only update if frame is actually rendered
                    # Calculate available width (account for padding ~40px)
                    available_width = max(400, main_frame_width - 40)
                    self.result_label.config(wraplength=available_width)
                    self.details_label.config(wraplength=available_width)
            except:
                pass  # Ignore errors during initial setup
        
        # Update wraplength on window resize
        self.main_frame.bind('<Configure>', update_wraplength)
        self.root.bind('<Configure>', update_wraplength)
        
        # Timestamp label (Feature 5) - more compact
        self.timestamp_label = tk.Label(
            self.result_card,
            text="",
            font=("Segoe UI", 8, "italic"),
            bg="#1a1a2e",
            fg="#7f8c8d"
        )
        # Don't pack initially, will be shown after scan
        
        # View Details button (Feature 4) - more compact
        self.view_details_button = tk.Button(
            self.result_card,
            text="📋 View Details",
            command=self.toggle_threat_details,
            font=("Segoe UI", 9),
            bg="#2d2d44",
            fg="#00d4ff",
            activebackground="#00d4ff",
            activeforeground="#1a1a2e",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=6,
            borderwidth=0
        )
        # Don't pack initially, will be shown after scan
        
        # Threat details frame (Feature 4) - expandable section
        self.threat_details_frame = tk.Frame(
            self.result_card,
            bg="#1a1a2e"
        )
        self.threat_details_visible = False
        
        # Threat details text widget with scrollbar - more compact
        details_scroll_frame = tk.Frame(self.threat_details_frame, bg="#1a1a2e")
        details_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        details_scrollbar = tk.Scrollbar(details_scroll_frame)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.threat_details_text = tk.Text(
            details_scroll_frame,
            font=("Consolas", 9),
            bg="#2d2d44",
            fg="#ffffff",
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=8,
            yscrollcommand=details_scrollbar.set,
            state=tk.DISABLED
        )
        self.threat_details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_scrollbar.config(command=self.threat_details_text.yview)
        
        # Copy Result button (initially hidden) - more compact
        self.copy_result_button = tk.Button(
            self.result_card,
            text="📋 Copy Result",
            command=self.copy_result_to_clipboard,
            font=("Segoe UI", 9),
            bg="#2d2d44",
            fg="#00d4ff",
            activebackground="#00d4ff",
            activeforeground="#1a1a2e",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=6,
            borderwidth=0
        )
        # Don't pack initially, will be shown after scan
        
        # Export button (Feature 7) - initially hidden - more compact
        self.export_button = tk.Button(
            self.result_card,
            text="📤 Export Result",
            command=self.export_result,
            font=("Segoe UI", 9),
            bg="#2d2d44",
            fg="#00ff88",
            activebackground="#00ff88",
            activeforeground="#1a1a2e",
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=6,
            borderwidth=0
        )
        
        # Batch results frame (Feature 6) - hidden by default
        self.batch_results_frame = tk.Frame(
            self.result_card,
            bg="#1a1a2e"
        )
        
        batch_results_label = tk.Label(
            self.batch_results_frame,
            text="📊 Batch Scan Results",
            font=("Segoe UI", 14, "bold"),
            bg="#1a1a2e",
            fg="#00d4ff"
        )
        batch_results_label.pack(pady=(10, 5))
        
        # Summary stats frame
        self.batch_summary_frame = tk.Frame(
            self.batch_results_frame,
            bg="#2d2d44",
            relief=tk.FLAT
        )
        self.batch_summary_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.batch_summary_label = tk.Label(
            self.batch_summary_frame,
            text="",
            font=("Segoe UI", 11),
            bg="#2d2d44",
            fg="#ffffff",
            justify=tk.LEFT
        )
        self.batch_summary_label.pack(pady=10, padx=15)
        
        # Progress label
        self.batch_progress_label = tk.Label(
            self.batch_results_frame,
            text="",
            font=("Segoe UI", 10, "italic"),
            bg="#1a1a2e",
            fg="#ffd700"
        )
        self.batch_progress_label.pack(pady=5)
        
        # Batch results list with scrollbar
        batch_scroll_frame = tk.Frame(self.batch_results_frame, bg="#1a1a2e")
        batch_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        batch_scrollbar = tk.Scrollbar(batch_scroll_frame)
        batch_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.batch_results_listbox = tk.Listbox(
            batch_scroll_frame,
            font=("Consolas", 9),
            bg="#2d2d44",
            fg="#ffffff",
            selectbackground="#00d4ff",
            selectforeground="#0f2027",
            relief=tk.FLAT,
            height=10,
            yscrollcommand=batch_scrollbar.set
        )
        self.batch_results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        batch_scrollbar.config(command=self.batch_results_listbox.yview)
        
        # Export batch button - more compact
        self.export_batch_button = tk.Button(
            self.batch_results_frame,
            text="📤 Export Batch Results",
            command=self.export_batch_results,
            font=("Segoe UI", 10, "bold"),
            bg="#00ff88",
            fg="#0f2027",
            activebackground="#00d4ff",
            activeforeground="#0f2027",
            cursor="hand2",
            relief=tk.FLAT,
            padx=25,
            pady=8,
            borderwidth=0
        )
        self.export_batch_button.pack(pady=10)
        
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
        self.export_button.pack_forget()  # Hide export button
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
    
    def clear_scan_history(self):
        """Clear all scan history with confirmation."""
        if messagebox.askyesno(
            "Clear History",
            "Are you sure you want to clear all scan history?\n\nThis action cannot be undone."
        ):
            if self.history.clear_history():
                self.refresh_history()
                self.load_recent_urls()  # Also refresh recent URLs dropdown
                self.set_status("✓ Scan history cleared", "#00ff88")
            else:
                self.set_status("Failed to clear history", "#ff6b6b")
                messagebox.showerror("Error", "Failed to clear scan history. Please try again.")
    
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
            self.threat_details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
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
        self.timestamp_label.pack(pady=(0, 8))
        
        # Feature 4: Populate threat details
        self.display_threat_details(verdict)
        
        # Show view details button
        self.view_details_button.pack(pady=(0, 8))
        
        # Show copy result button and export button - more compact
        button_row = tk.Frame(self.result_card, bg="#1a1a2e")
        button_row.pack(pady=(0, 12))
        self.copy_result_button.pack(in_=button_row, side=tk.LEFT, padx=4)
        self.export_button.pack(in_=button_row, side=tk.LEFT, padx=4)
    
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
        
        # Feature 8: Auto-format URL
        url = self.validator.format_url(url)
        self.url_var.set(url)
        
        # Clear previous results
        self.clear_results()
        
        # Disable button during processing
        self.disable_button()
        self.set_status("Initializing security scan...", "#ffd700")
        
        # Run analysis in background thread to prevent UI freezing
        thread = threading.Thread(target=self.analyze_url_thread, args=(url,), daemon=True)
        thread.start()
    
    # Feature 6: Batch mode methods
    def toggle_batch_mode(self):
        """Toggle between single and batch mode."""
        self.batch_mode = not self.batch_mode
        
        if self.batch_mode:
            # Switch to batch mode
            self.mode_toggle_button.config(text="🔗 Single Mode", bg="#ffd700")
            self.url_entry.pack_forget()
            self.recent_urls_button.place_forget()
            self.recent_urls_listbox_frame.pack_forget()
            self.validation_indicator.pack_forget()
            self.batch_input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            self.analyze_button.pack_forget()
            self.batch_analyze_button.pack(side=tk.LEFT, padx=5)
            self.clear_results()
        else:
            # Switch to single mode
            self.mode_toggle_button.config(text="📊 Batch Mode", bg="#2d2d44")
            self.batch_input_frame.pack_forget()
            self.url_entry.pack(fill=tk.X, ipady=12, ipadx=10)
            self.recent_urls_button.place(relx=0.98, rely=0.5, anchor=tk.E)
            self.validation_indicator.pack(fill=tk.X, padx=25, pady=(0, 10))
            self.batch_analyze_button.pack_forget()
            self.cancel_batch_button.pack_forget()
            self.analyze_button.pack(side=tk.LEFT, padx=5)
            self.clear_results()
            self.batch_results_frame.pack_forget()
    
    def analyze_batch(self):
        """Start batch URL analysis."""
        # Get URLs from text area
        text_content = self.batch_text.get("1.0", tk.END).strip()
        if not text_content:
            messagebox.showwarning("Input Required", "Please enter URLs to analyze (one per line).")
            return
        
        # Parse URLs
        urls = [line.strip() for line in text_content.split('\n') if line.strip()]
        
        if not urls:
            messagebox.showwarning("Input Required", "No valid URLs found.")
            return
        
        # Clear previous results
        self.batch_results = []
        self.cancel_batch = False
        self.batch_results_listbox.delete(0, tk.END)
        
        # Show batch results frame
        self.result_icon.config(text="")
        self.result_label.config(text="")
        self.details_label.config(text="")
        self.batch_results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Disable controls
        self.batch_text.config(state=tk.DISABLED)
        self.batch_analyze_button.pack_forget()
        self.cancel_batch_button.pack(side=tk.LEFT, padx=5)
        self.mode_toggle_button.config(state=tk.DISABLED)
        self.batch_processing = True
        
        # Start batch processing in background
        thread = threading.Thread(target=self.process_batch_urls, args=(urls,), daemon=True)
        thread.start()
    
    def process_batch_urls(self, urls):
        """Process multiple URLs sequentially."""
        total = len(urls)
        
        for i, url in enumerate(urls, 1):
            if self.cancel_batch:
                self.root.after(0, lambda: self.set_status("Batch processing cancelled", "#ff6b6b"))
                break
            
            # Update progress
            progress_text = f"Processing {i}/{total}..."
            self.root.after(0, lambda t=progress_text: self.batch_progress_label.config(text=t))
            self.root.after(0, lambda: self.set_status(f"Analyzing URL {i}/{total}...", "#ffd700"))
            
            try:
                # Format URL
                formatted_url = self.validator.format_url(url)
                
                # Analyze URL
                verdict = analyze_url_complete(formatted_url)
                
                # Extract data
                status = verdict.verdict if hasattr(verdict, 'verdict') else verdict.status
                threat_types = []
                if hasattr(verdict, 'api_data') and 'threat_types' in verdict.api_data:
                    threat_types = verdict.api_data.get('threat_types', [])
                
                rule_score = verdict.rule_based_score.get('total_score', 0) if hasattr(verdict, 'rule_based_score') else 0
                
                # Store result
                result = {
                    'url': formatted_url,
                    'status': status,
                    'threat_types': threat_types,
                    'rule_score': rule_score,
                    'timestamp': datetime.now().isoformat(),
                    'reasons': verdict.reasons if hasattr(verdict, 'reasons') else []
                }
                self.batch_results.append(result)
                
                # Save to history
                self.history.save_scan_to_history(formatted_url, verdict)
                
                # Display in listbox
                status_icons = {"safe": "✅", "suspicious": "⚠️", "dangerous": "🚫"}
                icon = status_icons.get(status, "❓")
                display_text = f"{icon} {status.upper()}: {formatted_url[:60]}"
                self.root.after(0, lambda dt=display_text: self.batch_results_listbox.insert(tk.END, dt))
                
            except Exception as e:
                error_result = {
                    'url': url,
                    'status': 'error',
                    'threat_types': [],
                    'rule_score': 0,
                    'timestamp': datetime.now().isoformat(),
                    'reasons': [f"Error: {str(e)}"]
                }
                self.batch_results.append(error_result)
                error_text = f"❌ ERROR: {url[:60]}"
                self.root.after(0, lambda et=error_text: self.batch_results_listbox.insert(tk.END, et))
        
        # Update summary
        self.root.after(0, self.update_batch_summary)
        self.root.after(0, self.finish_batch_processing)
    
    def update_batch_summary(self):
        """Update batch summary statistics."""
        total = len(self.batch_results)
        safe = sum(1 for r in self.batch_results if r['status'] == 'safe')
        suspicious = sum(1 for r in self.batch_results if r['status'] == 'suspicious')
        dangerous = sum(1 for r in self.batch_results if r['status'] == 'dangerous')
        errors = sum(1 for r in self.batch_results if r['status'] == 'error')
        
        summary_text = f"""Total URLs: {total}
✅ Safe: {safe}
⚠️ Suspicious: {suspicious}
🚫 Dangerous: {dangerous}"""
        if errors > 0:
            summary_text += f"\n❌ Errors: {errors}"
        
        self.batch_summary_label.config(text=summary_text)
        self.batch_progress_label.config(text="✓ Batch processing complete!", fg="#00ff88")
        self.set_status(f"Batch complete: {total} URLs scanned", "#00ff88")
        self.refresh_history()
    
    def finish_batch_processing(self):
        """Clean up after batch processing."""
        self.batch_processing = False
        self.batch_text.config(state=tk.NORMAL)
        self.cancel_batch_button.pack_forget()
        self.batch_analyze_button.pack(side=tk.LEFT, padx=5)
        self.mode_toggle_button.config(state=tk.NORMAL)
    
    def cancel_batch_processing(self):
        """Cancel ongoing batch processing."""
        self.cancel_batch = True
        self.batch_progress_label.config(text="Cancelling...", fg="#ff6b6b")
    
    # Feature 7: Export methods
    def export_result(self):
        """Export current scan result."""
        if not self.current_result:
            messagebox.showwarning("No Result", "No scan result available to export.")
            return
        
        # Ask for export format
        format_window = tk.Toplevel(self.root)
        format_window.title("Select Export Format")
        format_window.geometry("300x200")
        format_window.resizable(False, False)
        format_window.configure(bg="#1a1a2e")
        format_window.transient(self.root)
        format_window.grab_set()
        
        tk.Label(
            format_window,
            text="Select Export Format:",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        ).pack(pady=20)
        
        def export_as(fmt):
            format_window.destroy()
            self._perform_export(fmt)
        
        btn_frame = tk.Frame(format_window, bg="#1a1a2e")
        btn_frame.pack(expand=True)
        
        for fmt, label in [('json', '📄 JSON'), ('csv', '📊 CSV'), ('txt', '📝 TXT')]:
            tk.Button(
                btn_frame,
                text=label,
                command=lambda f=fmt: export_as(f),
                font=("Segoe UI", 11),
                bg="#00d4ff",
                fg="#0f2027",
                cursor="hand2",
                relief=tk.FLAT,
                padx=30,
                pady=10,
                width=12
            ).pack(pady=5)
    
    def _perform_export(self, format_type):
        """Perform the actual export operation."""
        # File dialog
        extensions = {
            'json': [("JSON files", "*.json")],
            'csv': [("CSV files", "*.csv")],
            'txt': [("Text files", "*.txt")]
        }
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=extensions.get(format_type, [("All files", "*.*")])
        )
        
        if not filepath:
            return
        
        # Prepare export data
        export_data = {
            'url': self.url_var.get().strip(),
            'status': self.current_result['status'],
            'threat_types': self.current_result['threats'],
            'timestamp': self.current_result['timestamp'],
            'rule_score': self.current_result.get('verdict').rule_based_score.get('total_score', 0) if hasattr(self.current_result.get('verdict'), 'rule_based_score') else 0,
            'reasons': self.current_result.get('verdict').reasons if hasattr(self.current_result.get('verdict'), 'reasons') else []
        }
        
        # Export
        success = False
        if format_type == 'json':
            success = ExportManager.export_to_json(filepath, export_data)
        elif format_type == 'csv':
            success = ExportManager.export_to_csv(filepath, export_data)
        elif format_type == 'txt':
            success = ExportManager.export_to_txt(filepath, export_data)
        
        if success:
            self.set_status(f"✓ Exported to {format_type.upper()}", "#00ff88")
            messagebox.showinfo("Export Success", f"Result exported successfully to:\n{filepath}")
        else:
            self.set_status("Export failed", "#ff6b6b")
            messagebox.showerror("Export Error", "Failed to export result. Please try again.")
    
    def export_batch_results(self):
        """Export batch scan results."""
        if not self.batch_results:
            messagebox.showwarning("No Results", "No batch results available to export.")
            return
        
        # Ask for export format
        format_window = tk.Toplevel(self.root)
        format_window.title("Select Export Format")
        format_window.geometry("300x200")
        format_window.resizable(False, False)
        format_window.configure(bg="#1a1a2e")
        format_window.transient(self.root)
        format_window.grab_set()
        
        tk.Label(
            format_window,
            text="Select Export Format:",
            font=("Segoe UI", 12, "bold"),
            bg="#1a1a2e",
            fg="#ffffff"
        ).pack(pady=20)
        
        def export_as(fmt):
            format_window.destroy()
            self._perform_batch_export(fmt)
        
        btn_frame = tk.Frame(format_window, bg="#1a1a2e")
        btn_frame.pack(expand=True)
        
        for fmt, label in [('json', '📄 JSON'), ('csv', '📊 CSV'), ('txt', '📝 TXT')]:
            tk.Button(
                btn_frame,
                text=label,
                command=lambda f=fmt: export_as(f),
                font=("Segoe UI", 11),
                bg="#00d4ff",
                fg="#0f2027",
                cursor="hand2",
                relief=tk.FLAT,
                padx=30,
                pady=10,
                width=12
            ).pack(pady=5)
    
    def _perform_batch_export(self, format_type):
        """Perform batch export operation."""
        extensions = {
            'json': [("JSON files", "*.json")],
            'csv': [("CSV files", "*.csv")],
            'txt': [("Text files", "*.txt")]
        }
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=extensions.get(format_type, [("All files", "*.*")])
        )
        
        if not filepath:
            return
        
        success = ExportManager.export_batch_results(filepath, self.batch_results, format_type)
        
        if success:
            self.set_status(f"✓ Batch exported to {format_type.upper()}", "#00ff88")
            messagebox.showinfo("Export Success", f"Batch results exported successfully to:\n{filepath}")
        else:
            self.set_status("Export failed", "#ff6b6b")
            messagebox.showerror("Export Error", "Failed to export batch results. Please try again.")
    
    # Feature 8: URL validation methods
    def on_url_change(self, *args):
        """Handle URL input changes for real-time validation."""
        url = self.url_var.get().strip()
        
        if not url or self.batch_mode:
            self.validation_indicator.config(text="")
            return
        
        # Validate URL
        self.validation_result = self.validator.validate_url(url)
        
        if self.validation_result.is_valid:
            if self.validation_result.warnings:
                # Valid but has warnings
                warning_text = f"⚠️ Warning: {self.validation_result.warnings[0]}"
                self.validation_indicator.config(text=warning_text, fg="#ffd700")
            else:
                # Completely valid
                self.validation_indicator.config(text="✓ Valid URL", fg="#00ff88")
        else:
            # Invalid URL
            if self.validation_result.errors:
                error_text = f"✗ {self.validation_result.errors[0]}"
                self.validation_indicator.config(text=error_text, fg="#ff6b6b")
            
            # Show suggestions if available
            if self.validation_result.suggestions and len(url) > 3:
                suggestion_text = f"💡 {self.validation_result.suggestions[0]}"
                self.validation_indicator.config(text=suggestion_text, fg="#00d4ff")
    
    # Feature 9: Recent URLs dropdown methods
    def load_recent_urls(self):
        """Load recent URLs from history."""
        recent_scans = self.history.get_recent_scans(15)
        self.recent_urls = [scan['url'] for scan in recent_scans]
    
    def toggle_recent_urls_dropdown(self):
        """Toggle recent URLs dropdown visibility."""
        if self.recent_urls_dropdown_visible:
            self.recent_urls_listbox_frame.pack_forget()
            self.recent_urls_button.config(text="▼")
            self.recent_urls_dropdown_visible = False
        else:
            # Refresh recent URLs
            self.load_recent_urls()
            
            # Populate listbox
            self.recent_urls_listbox.delete(0, tk.END)
            if self.recent_urls:
                for url in self.recent_urls:
                    display_url = url if len(url) <= 50 else url[:47] + "..."
                    self.recent_urls_listbox.insert(tk.END, display_url)
            else:
                self.recent_urls_listbox.insert(tk.END, "(No recent URLs)")
            
            # Show dropdown
            self.recent_urls_listbox_frame.pack(fill=tk.X, padx=25, pady=(0, 10))
            self.recent_urls_button.config(text="▲")
            self.recent_urls_dropdown_visible = True
    
    def on_recent_url_select(self, event):
        """Handle selection from recent URLs dropdown."""
        selection = self.recent_urls_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.recent_urls):
            selected_url = self.recent_urls[index]
            self.url_var.set(selected_url)
            self.toggle_recent_urls_dropdown()  # Close dropdown
    
    def show_recent_urls_context_menu(self, event):
        """Show context menu for recent URLs (clear history option)."""
        menu = tk.Menu(self.root, tearoff=0, bg="#2d2d44", fg="#ffffff")
        menu.add_command(label="Clear History", command=self.clear_recent_urls_history)
        menu.post(event.x_root, event.y_root)
    
    def clear_recent_urls_history(self):
        """Clear recent URLs history."""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all recent URLs?"):
            self.history.clear_history()
            self.recent_urls = []
            self.recent_urls_listbox.delete(0, tk.END)
            self.recent_urls_listbox.insert(tk.END, "(No recent URLs)")
            self.refresh_history()
            self.set_status("History cleared", "#00ff88")


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = LinkSafetyCheckerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
