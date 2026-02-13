import requests
import os
from datetime import datetime

# --- CONFIG ---
URL = "https://www.stwdo.de/en/living-houses-application/current-housing-offers"
TARGET_TEXT = "No results found for the given search criteria"
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")

def send_notification():
    """Send push notification via ntfy.sh"""
    if not NTFY_TOPIC:
        print(f"⚠ NTFY_TOPIC not set — skipping notification")
        return False

    try:
        resp = requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data="🏠 NEW APARTMENT! Check STWDO now!",
            headers={"Title": "Housing Alert", "Tags": "house"},
            timeout=5
        )
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"✗ Notification failed: {e}")
        return False

def check():
    """Check STWDO website for new housing listings"""
    try:
        response = requests.get(
            URL,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=10
        )
        response.raise_for_status()

        if TARGET_TEXT.lower() not in response.text.lower():
            sent = send_notification()
            status = "ALERT SENT" if sent else "ALERT (notification skipped)"
            print(f"🏠 {status} - {datetime.now().isoformat()}")
        else:
            print(f"✓ No change - {datetime.now().isoformat()}")

    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Connection failed: {e}")
    except requests.exceptions.Timeout as e:
        print(f"✗ Request timed out: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

if __name__ == "__main__":
    check()
