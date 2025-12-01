"""History management module for Link Safety Checker GUI."""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional


class ScanHistory:
    """Manages scan history storage and retrieval."""
    
    def __init__(self, history_file: str = "scan_history.json", max_scans: int = 100):
        """Initialize the scan history manager.
        
        Args:
            history_file: Path to the history JSON file
            max_scans: Maximum number of scans to keep in history
        """
        self.history_file = Path(history_file)
        self.max_scans = max_scans
        self._ensure_history_file()
    
    def _ensure_history_file(self):
        """Create history file if it doesn't exist."""
        if not self.history_file.exists():
            initial_data = {
                "scans": [],
                "metadata": {
                    "version": "1.0",
                    "max_scans": self.max_scans
                }
            }
            try:
                with open(self.history_file, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, indent=2)
            except Exception as e:
                print(f"Error creating history file: {e}")
    
    def save_scan_to_history(self, url: str, verdict: Any) -> bool:
        """Save a scan result to history.
        
        Args:
            url: The URL that was scanned
            verdict: The verdict object from the analysis
            
        Returns:
            True if save was successful, False otherwise
        """
        try:
            # Load existing history
            history_data = self._load_history_data()
            
            # Extract status and threat types from verdict
            status = verdict.verdict if hasattr(verdict, 'verdict') else verdict.status
            threat_types = []
            if hasattr(verdict, 'api_data') and 'threat_types' in verdict.api_data:
                threat_types = verdict.api_data.get('threat_types', [])
            elif hasattr(verdict, 'threat_types'):
                threat_types = verdict.threat_types
            
            # Create scan entry
            scan_entry = {
                "url": url,
                "status": status,
                "threat_types": threat_types,
                "timestamp": datetime.now().isoformat(),
                "result": {
                    "verdict": status,
                    "threat_types": threat_types,
                    "rule_score": verdict.rule_based_score.get('total_score', 0) if hasattr(verdict, 'rule_based_score') else 0
                }
            }
            
            # Add to history
            history_data["scans"].insert(0, scan_entry)  # Insert at beginning
            
            # Enforce max scans limit
            if len(history_data["scans"]) > self.max_scans:
                history_data["scans"] = history_data["scans"][:self.max_scans]
            
            # Save back to file
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving scan to history: {e}")
            return False
    
    def _load_history_data(self) -> Dict[str, Any]:
        """Load history data from file.
        
        Returns:
            Dictionary containing history data
        """
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure structure is correct
                if "scans" not in data:
                    data["scans"] = []
                if "metadata" not in data:
                    data["metadata"] = {"version": "1.0", "max_scans": self.max_scans}
                return data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading history, creating new file: {e}")
            # Return empty history if file is corrupted
            return {
                "scans": [],
                "metadata": {
                    "version": "1.0",
                    "max_scans": self.max_scans
                }
            }
    
    def load_scan_history(self) -> List[Dict[str, Any]]:
        """Load all scan history.
        
        Returns:
            List of scan entries
        """
        data = self._load_history_data()
        return data.get("scans", [])
    
    def get_recent_scans(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent N scans.
        
        Args:
            count: Number of recent scans to retrieve
            
        Returns:
            List of recent scan entries
        """
        scans = self.load_scan_history()
        return scans[:count]
    
    def clear_history(self) -> bool:
        """Clear all scan history.
        
        Returns:
            True if clear was successful, False otherwise
        """
        try:
            data = {
                "scans": [],
                "metadata": {
                    "version": "1.0",
                    "max_scans": self.max_scans
                }
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False
