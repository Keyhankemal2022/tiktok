# TikTok Auto Like and Follow Bot

This is a Python automation script that uses Selenium to log into TikTok, follow a specified user, and like all their videos automatically.

---

## Features

- Logs into TikTok with your credentials.
- Follows the specified TikTok username if not already following.
- Likes every video on that user's profile if not liked already.
- Handles page navigation and loading.
- Requires manual handling of CAPTCHA or 2FA during login if prompted.

---

## Requirements

- Python 3.x
- Google Chrome browser installed
- ChromeDriver matching your Chrome version (https://chromedriver.chromium.org/downloads)
- Selenium Python package

---

## Installation

1. **Clone or download this repository.**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
