import requests
import os
import sys

# --- CONFIGURATION ---
# Currently set to your TEST GIST. 
# When you are done testing, replace this with the real STWDO URL.
URL = "https://gist.githubusercontent.com/rushi-k-op/0b9cda9f72887ad6431a3bb714d40ce0/raw/1e9fd12c12753d5f8cdb4133c8206ed0c007f5ba/status.txt"

# The text we expect to see if there are NO apartments.
TARGET_TEXT = "No results found for the given search criteria"

# Get the secret topic from GitHub Settings
NTFY_TOPIC = os.environ.get("NTFY_TOPIC")

def send_notification():
    if not NTFY_TOPIC:
        print("Error: NTFY_TOPIC is missing from Settings.")
        return

    print(f"Sending notification to ntfy.sh/{NTFY_TOPIC}...")
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data="Test successful. The website content has changed.",
            headers={
                "Title": "System Check OK",
                "Priority": "high",
                "Tags": "warning"
            },
            timeout=10
        )
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def check_website():
    print(f"Checking URL: {URL}")
    
    try:
        response = requests.get(URL, timeout=10)
        # Fix encoding issues by forcing UTF-8
        response.encoding = 'utf-8' 
        page_content = response.text
        
        print(f"Page content found: '{page_content.strip()}'")

        if TARGET_TEXT in page_content:
            print(f"Status: No change. Found '{TARGET_TEXT}'.")
        else:
            print(f"Status: Change detected. '{TARGET_TEXT}' is missing.")
            send_notification()

    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_website()
