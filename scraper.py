import requests
import os
import sys
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
URL = "https://www.stwdo.de/en/living-houses-application/current-housing-offers"
TARGET_TEXT = "No results found for the given search criteria"

# We fetch the secret topic from the environment.
# This keeps your personal notification channel private, even if the code is public.
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")

def send_notification():
    """Sends a push notification to your phone via ntfy.sh"""
    if not NTFY_TOPIC:
        print("Error: NTFY_TOPIC is missing. Notification skipped.")
        return

    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data="New content detected on STWDO housing page! Check immediately.",
            headers={
                "Title": "🏠 STWDO Housing Alert",
                "Priority": "high",
                "Tags": "house,rotating_light",
                "Click": URL
            },
            timeout=10
        )
        print(f"Notification sent successfully to topic ending in ...{NTFY_TOPIC[-4:]}")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def check_website():
    """Checks if the 'No results' text is missing from the page."""
    print(f"Checking {URL}...")
    
    # We use a standard browser User-Agent to avoid being blocked.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()

        # LOGIC: If the "No results" text is NOT found, it means there are listings.
        if TARGET_TEXT not in page_text:
            print("🚨 CHANGE DETECTED: The 'No results' text is gone!")
            send_notification()
        else:
            print("✅ No change: 'No results' text is still there.")

    except Exception as e:
        print(f"❌ Error checking website: {e}")
        # We exit with code 1 so GitHub Actions knows the script failed
        sys.exit(1)

if __name__ == "__main__":
    check_website()
