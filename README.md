# Student Housing Tracker

An automated housing monitor that checks rental listing pages on a schedule and sends push notifications to your phone the moment a new listing appears. No server required, no costs involved -- just GitHub Actions and a free notification service.

## Background

Finding an apartment in Germany as an international student is tough. When I discovered that Studentenwohnheime (student dormitories) exist and are affordable, I was relieved -- until I learned that listings work on a first-come, first-served basis. Whoever applies first gets the apartment. Constantly refreshing the website was not realistic, so I built this tool to do it for me.

This project was originally built to monitor the [Studierendenwerk Dortmund (STWDO)](https://www.stwdo.de/en/living-houses-application/current-housing-offers) housing portal, but it can be adapted to monitor any website where you need to detect when new content appears.

## How It Works

1. A GitHub Actions workflow runs every 5 minutes (configurable via cron).
2. The Python scraper fetches the target housing page.
3. It checks whether the page still contains a specific "no results" message.
4. If that message is **absent**, it means a new listing is likely available -- a push notification is sent to your phone via [ntfy.sh](https://ntfy.sh).
5. If nothing has changed, it logs the result and exits quietly.

## Project Structure

```
student-housing-tracker/
├── .github/
│   └── workflows/
│       └── monitor.yml      # GitHub Actions workflow (runs every 5 min)
├── scraper.py                # Main scraper and notification logic
└── requirements.txt          # Python dependencies
```

## Setup Instructions

### Prerequisites

- A GitHub account with the **GitHub Student Developer Pack** (see note below)
- A smartphone or browser to receive notifications

### Step 1 -- Fork or clone this repository

```bash
git clone https://github.com/rushi-k-op/stwdo-tracker.git
cd stwdo-tracker
```

### Step 2 -- Configure the scraper

Open `scraper.py` and update these two variables to match the website you want to monitor:

```python
URL = "https://example.com/housing-listings"
TARGET_TEXT = "No results found"
```

- `URL` -- the page you want to check for new listings.
- `TARGET_TEXT` -- the text that appears on the page when there are **no** listings available. When this text disappears, the scraper assumes a new listing has been posted.

### Step 3 -- Choose an ntfy topic

Pick a unique, hard-to-guess topic name for your notifications. This acts as your private channel.

Example: `housing-yourname-x7k2`

### Step 4 -- Add the topic as a GitHub secret

1. Go to your repository on GitHub.
2. Navigate to **Settings > Secrets and variables > Actions**.
3. Click **New repository secret**.
4. Name: `NTFY_TOPIC`
5. Value: your chosen topic name (just the name, not the full URL)
6. Click **Add secret**.

### Step 5 -- Subscribe to your ntfy topic

Install the ntfy app on your phone and subscribe to your topic:

- **Android** -- [ntfy on Google Play](https://play.google.com/store/apps/details?id=io.heckel.ntfy)
- **iOS** -- [ntfy on the App Store](https://apps.apple.com/us/app/ntfy/id1625396347)
- **Web** -- open `https://ntfy.sh/your-topic-name` in any browser

Tested and confirmed working on Android and the web client. The iOS app should work the same way.

### Step 6 -- Enable the workflow

The GitHub Actions workflow should start running automatically after you push your changes. You can also trigger it manually:

1. Go to the **Actions** tab in your repository.
2. Select **Housing Monitor**.
3. Click **Run workflow**.

### Testing locally

```bash
pip install -r requirements.txt
export NTFY_TOPIC="your-topic-name"
python scraper.py
```

If there are no new listings, you should see:

```
No change - 2026-02-13T15:55:56.732179
```

## Tech Stack

- **Python 3.12** -- scraper and notification logic
- **Requests** -- HTTP library for fetching pages and sending notifications
- **GitHub Actions** -- scheduled execution (cron-based, every 5 minutes)
- **ntfy.sh** -- free, open-source push notification service (no account required)

## A Note on the GitHub Student Developer Pack

This project is designed by a student, for students. It relies on GitHub Actions to run the scraper on a schedule. GitHub Free accounts have limited Actions minutes per month, which may not be enough for a job that runs every 5 minutes. With the [GitHub Student Developer Pack](https://education.github.com/pack), you get significantly more Actions minutes at no cost, which makes this project practical to run continuously.

I am currently exploring alternatives that do not depend on GitHub Actions minutes, so that anyone can use this regardless of their plan.

## Responsible Use

Please be respectful when using this tool or adapting it for other websites. Always review and follow the target website's terms of service, privacy policy, and robots.txt. Avoid sending excessive requests that could burden a server. This tool is intended for personal, low-frequency use and should not be used to scrape data at scale or in ways that violate any website's bot or usage policies.

## License

This project does not currently include a license. If you would like to reuse or contribute, please reach out.