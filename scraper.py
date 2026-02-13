import requests
import os
import sys

# --- CONFIGURATION ---
# PASTE YOUR GIST RAW URL HERE!
URL = "https://gist.githubusercontent.com/rushi-k-op/0b9cda9f72887ad6431a3bb714d40ce0/raw/05718923d17c761d0082e85f3d0d7bf125e6b1ad/status.txt" 

# The "Safety Phrase". If this exists, we assume NO apartments.
TARGET_TEXT = "No results found for the given search criteria"

# Get the secret topic from GitHub Settings
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")

def send_notification():
    if not NTFY_TOPIC:
        print("❌ ERROR: NTFY_TOPIC is missing from Settings!")
        return

    print(f"🔔 Sending notification to: https://ntfy.sh/{NTFY_TOPIC}")
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data="TEST SUCCESSFUL! The website changed!",
            headers={
                "Title": "✅ System Works!",
                "Priority": "high",
                "Tags": "tada,check_mark"
            },
            timeout=10
        )
        print("✅ Notification sent! Check your phone.")
    except Exception as e:
        print(f"❌ Failed to send notification: {e}")

def check_website():
    print(f"🔎 Checking URL: {URL}")
    
    try:
        response = requests.get(URL, timeout=10)
        page_content = response.text
        
        print(f"📄 Page Content Found: '{page_content.strip()}'")

        if TARGET_TEXT in page_content:
            print(f"✅ Safe: Found the text '{TARGET_TEXT}'. No notification needed.")
        else:
            print(f"🚨 ALERT: '{TARGET_TEXT}' is MISSING! Sending alert...")
            send_notification()

    except Exception as e:
        print(f"❌ Crash: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_website()
