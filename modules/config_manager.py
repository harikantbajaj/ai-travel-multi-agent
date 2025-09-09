"""
Configuration Manager Module
Handles application configuration and settings
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages application configuration"""

    def __init__(self, config_file: str = "config/travel_agent_config.json"):
        self.config_file = Path(config_file)
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = self.get_default_config()
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = self.get_default_config()

    def save_config(self):
        """Save configuration to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "api_keys": {
                "weather_api_key": os.getenv("OPENWEATHER_API_KEY", ""),
                "maps_api_key": os.getenv("GOOGLE_PLACES_API_KEY", ""),
                "currency_api_key": os.getenv("EXCHANGERATE_API_KEY", ""),
                "gemini_api_key": os.getenv("GEMINI_API_KEY", "")
            },
            "settings": {
                "default_currency": "USD",
                "default_budget_multiplier": 1.2,
                "max_attractions_per_day": 3,
                "max_restaurants_per_day": 2,
                "search_radius_km": 50,
                "weather_forecast_days": 7
            },
            "export_formats": ["txt", "json", "pdf"],
            "agent_modes": {
                "single_agent": True,
                "multi_agent_legacy": True,
                "langgraph_agent": True
            }
        }

    def get(self, key: str, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
