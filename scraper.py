import requests
import os
import sys
from datetime import datetime

# --- CONFIG ---
URL = "https://www.stwdo.de/en/living-houses-application/current-housing-offers"
TARGET_TEXT = "No results found for the given search criteria"
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")

def send_notification():
    """Simple notification - no extra imports needed"""
    if not NTFY_TOPIC:
        return
    
    try:
        # Ultra simple POST request
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=" NEW APARTMENT! Check STWDO now!",
            headers={"Title": "Housing Alert", "Tags": "house"},
            timeout=5  # Short timeout to save time
        )
    except:
        pass  # Fail silently, no need to log

def check():
    """Single function, minimal operations"""
    try:
        # Minimal headers
        response = requests.get(
            URL, 
            headers={'User-Agent': 'Mozilla/5.0'}, 
            timeout=10
        )
        
        # Quick check (case-insensitive)
        if TARGET_TEXT.lower() not in response.text.lower():
            send_notification()
            print(f" ALERT SENT - {datetime.now().isoformat()}")
        else:
            print(f" No change - {datetime.now().isoformat()}")
            
    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    check()
