"""
Export Manager Module
Handles exporting trip plans in various formats
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class ExportManager:
    """Manages exporting trip plans in different formats"""

    def __init__(self):
        self.output_dir = Path("exports")
        self.output_dir.mkdir(exist_ok=True)

    def export_text(self, summary, filename: str):
        """Export trip plan as text file"""
        try:
            content = self._generate_text_content(summary)
            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Text export saved to: {filepath}")
        except Exception as e:
            print(f"Error exporting text: {e}")

    def export_json(self, summary, filename: str):
        """Export trip plan as JSON file"""
        try:
            # Convert summary object to dict if needed
            if hasattr(summary, '__dict__'):
                data = self._object_to_dict(summary)
            else:
                data = summary

            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            print(f"JSON export saved to: {filepath}")
        except Exception as e:
            print(f"Error exporting JSON: {e}")

    def export_pdf(self, summary, filename: str):
        """Export trip plan as PDF file"""
        try:
            # For now, create a simple text-based PDF representation
            # In a real implementation, you'd use a PDF library like reportlab
            content = self._generate_text_content(summary)
            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("PDF Export (Text Format)\n")
                f.write("=" * 50 + "\n\n")
                f.write(content)
            print(f"PDF export saved to: {filepath}")
        except Exception as e:
            print(f"Error exporting PDF: {e}")

    def prepare_email_summary(self, summary, trip_details: Dict):
        """Prepare trip summary for email"""
        try:
            content = self._generate_text_content(summary)
            # In a real implementation, you'd integrate with email service
            print("Email summary prepared (not sent - email integration needed)")
            return content
        except Exception as e:
            print(f"Error preparing email: {e}")

    def export_mobile_html(self, summary, filename: str):
        """Export trip plan as mobile-friendly HTML"""
        try:
            html_content = self._generate_html_content(summary)
            filepath = self.output_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Mobile HTML export saved to: {filepath}")
        except Exception as e:
            print(f"Error exporting mobile HTML: {e}")

    def _generate_text_content(self, summary) -> str:
        """Generate text content from summary"""
        content = f"""
TRAVEL PLAN SUMMARY
{'='*50}

Destination: {getattr(summary, 'destination', 'N/A')}
Dates: {getattr(summary, 'start_date', 'N/A')} to {getattr(summary, 'end_date', 'N/A')}
Duration: {getattr(summary, 'total_days', 'N/A')} days
Travelers: {getattr(summary, 'num_travelers', 1)}
Estimated Cost: {getattr(summary, 'converted_total', 'N/A')} {getattr(summary, 'currency', 'USD')}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return content

    def _generate_html_content(self, summary) -> str:
        """Generate HTML content for mobile"""
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travel Plan - {getattr(summary, 'destination', 'Trip')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
        .section {{ margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Travel Plan</h1>
        <p><strong>Destination:</strong> {getattr(summary, 'destination', 'N/A')}</p>
        <p><strong>Dates:</strong> {getattr(summary, 'start_date', 'N/A')} to {getattr(summary, 'end_date', 'N/A')}</p>
        <p><strong>Estimated Cost:</strong> {getattr(summary, 'converted_total', 'N/A')} {getattr(summary, 'currency', 'USD')}</p>
    </div>
    <div class="section">
        <p>This is a mobile-friendly travel plan summary.</p>
    </div>
</body>
</html>
"""
        return html

    def _object_to_dict(self, obj) -> Dict[str, Any]:
        """Convert object to dictionary"""
        if hasattr(obj, '__dict__'):
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    if hasattr(value, '__dict__'):
                        result[key] = self._object_to_dict(value)
                    else:
                        result[key] = value
            return result
        return obj
