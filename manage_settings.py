import json
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    """Load settings from the JSON file."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        # Default settings if the file doesn't exist
        return {
            "default_location": "",
            "temperature_unit": "metric",
            "favorite_locations": []
        }

def save_settings(settings):
    """Save settings to the JSON file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)
    print(f"Settings saved: {settings}")  # Debugging log