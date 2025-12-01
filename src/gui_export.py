"""Export functionality module for Link Safety Checker GUI."""
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class ExportManager:
    """Manages export functionality for scan results."""
    
    @staticmethod
    def export_to_json(filepath: str, scan_data: Dict[str, Any]) -> bool:
        """Export scan result to JSON format.
        
        Args:
            filepath: Path where the JSON file will be saved
            scan_data: Dictionary containing scan result data
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            # Prepare JSON structure
            export_data = {
                "scan_date": scan_data.get('timestamp', datetime.now().isoformat()),
                "url": scan_data.get('url', ''),
                "status": scan_data.get('status', 'unknown'),
                "threat_types": scan_data.get('threat_types', []),
                "details": {
                    "rule_score": scan_data.get('rule_score', 0),
                    "verdict": scan_data.get('status', 'unknown'),
                    "api_available": scan_data.get('api_available', False),
                    "reasons": scan_data.get('reasons', [])
                },
                "metadata": {
                    "export_date": datetime.now().isoformat(),
                    "tool": "Link Safety Checker - AlesSystems",
                    "version": "1.0"
                }
            }
            
            # Write to file with pretty formatting
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return False
    
    @staticmethod
    def export_to_csv(filepath: str, scan_data: Dict[str, Any]) -> bool:
        """Export scan result to CSV format.
        
        Args:
            filepath: Path where the CSV file will be saved
            scan_data: Dictionary containing scan result data
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            # Prepare CSV data
            threat_types_str = ", ".join(scan_data.get('threat_types', []))
            timestamp = scan_data.get('timestamp', datetime.now().isoformat())
            
            # Check if file exists to determine if we need headers
            file_exists = Path(filepath).exists()
            
            with open(filepath, 'a' if file_exists else 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header if new file
                if not file_exists:
                    writer.writerow(['URL', 'Status', 'Threat Types', 'Risk Score', 'Timestamp'])
                
                # Write data row
                writer.writerow([
                    scan_data.get('url', ''),
                    scan_data.get('status', 'unknown').upper(),
                    threat_types_str if threat_types_str else 'None',
                    scan_data.get('rule_score', 0),
                    timestamp
                ])
            
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    @staticmethod
    def export_to_txt(filepath: str, scan_data: Dict[str, Any]) -> bool:
        """Export scan result to TXT format (human-readable report).
        
        Args:
            filepath: Path where the TXT file will be saved
            scan_data: Dictionary containing scan result data
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            # Prepare formatted text report
            lines = []
            lines.append("=" * 70)
            lines.append("LINK SAFETY CHECKER - SCAN REPORT")
            lines.append("Developed by AlesSystems")
            lines.append("=" * 70)
            lines.append("")
            
            # URL Information
            lines.append("URL INFORMATION")
            lines.append("-" * 70)
            lines.append(f"URL: {scan_data.get('url', 'N/A')}")
            lines.append(f"Scan Date: {scan_data.get('timestamp', datetime.now().isoformat())}")
            lines.append("")
            
            # Security Status
            lines.append("SECURITY STATUS")
            lines.append("-" * 70)
            status = scan_data.get('status', 'unknown').upper()
            status_symbols = {
                'SAFE': '✅ SAFE TO VISIT',
                'SUSPICIOUS': '⚠️ POTENTIALLY SUSPICIOUS',
                'DANGEROUS': '🚫 DANGEROUS - DO NOT VISIT'
            }
            lines.append(f"Status: {status_symbols.get(status, status)}")
            lines.append(f"Risk Score: {scan_data.get('rule_score', 0)}/100")
            lines.append("")
            
            # Threat Information
            lines.append("THREAT INFORMATION")
            lines.append("-" * 70)
            threat_types = scan_data.get('threat_types', [])
            if threat_types:
                lines.append("Detected Threats:")
                for i, threat in enumerate(threat_types, 1):
                    lines.append(f"  {i}. {threat}")
            else:
                lines.append("No threats detected")
            lines.append("")
            
            # Analysis Details
            reasons = scan_data.get('reasons', [])
            if reasons:
                lines.append("ANALYSIS DETAILS")
                lines.append("-" * 70)
                for reason in reasons:
                    lines.append(f"• {reason}")
                lines.append("")
            
            # Recommendations
            lines.append("RECOMMENDATIONS")
            lines.append("-" * 70)
            if status == 'SAFE':
                lines.append("✓ This link appears safe to visit")
                lines.append("✓ No known threats detected")
            elif status == 'SUSPICIOUS':
                lines.append("⚠ Exercise caution when visiting this link")
                lines.append("⚠ Verify the source before proceeding")
                lines.append("⚠ Do not enter sensitive information")
            elif status == 'DANGEROUS':
                lines.append("🚫 DO NOT VISIT THIS LINK")
                lines.append("🚫 This site may harm your computer")
                lines.append("🚫 Report this link to authorities if received via email/message")
            lines.append("")
            
            # Footer
            lines.append("=" * 70)
            lines.append(f"Report Generated: {datetime.now().strftime('%b %d, %Y at %I:%M %p')}")
            lines.append("=" * 70)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            return True
            
        except Exception as e:
            print(f"Error exporting to TXT: {e}")
            return False
    
    @staticmethod
    def export_batch_results(filepath: str, batch_results: List[Dict[str, Any]], 
                            format_type: str = 'json') -> bool:
        """Export multiple scan results (batch export).
        
        Args:
            filepath: Path where the file will be saved
            batch_results: List of scan result dictionaries
            format_type: Export format ('json', 'csv', or 'txt')
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            if format_type.lower() == 'json':
                return ExportManager._export_batch_json(filepath, batch_results)
            elif format_type.lower() == 'csv':
                return ExportManager._export_batch_csv(filepath, batch_results)
            elif format_type.lower() == 'txt':
                return ExportManager._export_batch_txt(filepath, batch_results)
            else:
                print(f"Unsupported format: {format_type}")
                return False
                
        except Exception as e:
            print(f"Error in batch export: {e}")
            return False
    
    @staticmethod
    def _export_batch_json(filepath: str, batch_results: List[Dict[str, Any]]) -> bool:
        """Export batch results to JSON."""
        try:
            export_data = {
                "batch_scan_date": datetime.now().isoformat(),
                "total_scans": len(batch_results),
                "summary": {
                    "safe": sum(1 for r in batch_results if r.get('status') == 'safe'),
                    "suspicious": sum(1 for r in batch_results if r.get('status') == 'suspicious'),
                    "dangerous": sum(1 for r in batch_results if r.get('status') == 'dangerous')
                },
                "results": batch_results,
                "metadata": {
                    "export_date": datetime.now().isoformat(),
                    "tool": "Link Safety Checker - AlesSystems",
                    "version": "1.0"
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error in batch JSON export: {e}")
            return False
    
    @staticmethod
    def _export_batch_csv(filepath: str, batch_results: List[Dict[str, Any]]) -> bool:
        """Export batch results to CSV."""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(['URL', 'Status', 'Threat Types', 'Risk Score', 'Timestamp'])
                
                # Write data rows
                for result in batch_results:
                    threat_types_str = ", ".join(result.get('threat_types', []))
                    writer.writerow([
                        result.get('url', ''),
                        result.get('status', 'unknown').upper(),
                        threat_types_str if threat_types_str else 'None',
                        result.get('rule_score', 0),
                        result.get('timestamp', '')
                    ])
            
            return True
        except Exception as e:
            print(f"Error in batch CSV export: {e}")
            return False
    
    @staticmethod
    def _export_batch_txt(filepath: str, batch_results: List[Dict[str, Any]]) -> bool:
        """Export batch results to TXT."""
        try:
            lines = []
            lines.append("=" * 70)
            lines.append("LINK SAFETY CHECKER - BATCH SCAN REPORT")
            lines.append("Developed by AlesSystems")
            lines.append("=" * 70)
            lines.append("")
            
            # Summary
            safe_count = sum(1 for r in batch_results if r.get('status') == 'safe')
            suspicious_count = sum(1 for r in batch_results if r.get('status') == 'suspicious')
            dangerous_count = sum(1 for r in batch_results if r.get('status') == 'dangerous')
            
            lines.append("BATCH SUMMARY")
            lines.append("-" * 70)
            lines.append(f"Total URLs Scanned: {len(batch_results)}")
            lines.append(f"✅ Safe: {safe_count}")
            lines.append(f"⚠️ Suspicious: {suspicious_count}")
            lines.append(f"🚫 Dangerous: {dangerous_count}")
            lines.append(f"Scan Date: {datetime.now().strftime('%b %d, %Y at %I:%M %p')}")
            lines.append("")
            
            # Individual Results
            lines.append("DETAILED RESULTS")
            lines.append("=" * 70)
            lines.append("")
            
            for i, result in enumerate(batch_results, 1):
                status = result.get('status', 'unknown').upper()
                status_symbols = {
                    'SAFE': '✅',
                    'SUSPICIOUS': '⚠️',
                    'DANGEROUS': '🚫'
                }
                symbol = status_symbols.get(status, '❓')
                
                lines.append(f"[{i}] {symbol} {status}")
                lines.append(f"URL: {result.get('url', 'N/A')}")
                lines.append(f"Risk Score: {result.get('rule_score', 0)}/100")
                
                threat_types = result.get('threat_types', [])
                if threat_types:
                    lines.append(f"Threats: {', '.join(threat_types)}")
                
                lines.append("")
            
            lines.append("=" * 70)
            lines.append(f"Report Generated: {datetime.now().strftime('%b %d, %Y at %I:%M %p')}")
            lines.append("=" * 70)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            return True
        except Exception as e:
            print(f"Error in batch TXT export: {e}")
            return False
