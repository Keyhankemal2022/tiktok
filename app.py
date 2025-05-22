"""
TikTok Auto Like and Follow Bot using Selenium

This script:
- Logs into TikTok with your username and password.
- Goes to a target user's profile.
- Follows the user if not already following.
- Likes every video on that user's profile if not already liked.

Requirements:
- Python 3.x
- Selenium package (`pip install selenium`)
- Chrome browser installed
- ChromeDriver executable matching your Chrome version: https://chromedriver.chromium.org/downloads
  Make sure chromedriver is in your PATH or specify its path in the script.

WARNING:
- Automating TikTok actions can violate TikTok terms and may get your account banned.
- Use responsibly and at your own risk.

Usage:
- Run `python tiktok_auto_like_follow.py`
- Input your TikTok username and password when prompted.
- Input the TikTok username you want to follow and like videos for.

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import getpass

def login_tiktok(driver, username, password):
    driver.get("https://www.tiktok.com/login")

    wait = WebDriverWait(driver, 30)

    # Wait for login form to load and click "Use phone / email / username" login method
    try:
        # There may be multiple login options - choose the username/password option
        # This might require clicking a button - sometimes TikTok presents QR code login by default
        use_account_login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Use phone / email / username')]")))
        use_account_login_button.click()
    except Exception:
        # If not found, maybe it already shows username password login
        pass

    # Wait for username input
    try:
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.clear()
        username_input.send_keys(username)
    except Exception as e:
        print("Error locating username input:", e)
        return False

    # Password input
    try:
        password_input = driver.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(password)
    except Exception as e:
        print("Error locating password input:", e)
        return False

    # Click login button
    try:
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
    except Exception as e:
        print("Error locating login button:", e)
        return False

    # Wait for potential 2FA, captcha - user may need to intervene manually here
    print("Waiting for login to complete... please complete any captcha or 2FA if required.")
    time.sleep(20)

    # Check if login successful by looking for home page element
    if "login" in driver.current_url.lower():
        print("Login failed - please check credentials or complete login manually.")
        return False
    print("Login successful!")
    return True

def follow_user(driver, target_username):
    driver.get(f"https://www.tiktok.com/@{target_username}")

    wait = WebDriverWait(driver, 20)
    try:
        # Wait for follow button visible and clickable
        follow_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Follow')]")))
        # Check if button indicates already following
        if "Following" in follow_btn.text or "Requested" in follow_btn.text:
            print(f"Already following or request pending on user {target_username}.")
            return
        follow_btn.click()
        print(f"Followed user: {target_username}")
        time.sleep(2)  # Give time after clicking
    except Exception as e:
        print(f"Could not follow user {target_username}: {e}")

def like_all_videos(driver, target_username):
    driver.get(f"https://www.tiktok.com/@{target_username}")

    wait = WebDriverWait(driver, 20)
    time.sleep(5) 

    # Scroll down to load videos
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_pause_time = 2

    # Scroll to load videos multiple times
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Locate all video thumbnails
    try:
        video_links = driver.find_elements(By.XPATH, "//div[contains(@data-e2e,'user-post-item')]//a")
        print(f"Found {len(video_links)} videos on user {target_username}.")
    except Exception as e:
        print("Error finding videos:", e)
        return

    for idx, video_link in enumerate(video_links):
        try:
            video_url = video_link.get_attribute("href")
            print(f"Processing video {idx +1}: {video_url}")
            driver.get(video_url)
            time.sleep(5)  # Wait for video page to load

            # Find like button
            try:
                like_button = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@data-e2e,'like-icon')]")))
                aria_pressed = like_button.get_attribute("aria-pressed")
                # aria-pressed="true" means liked
                if aria_pressed == "true":
                    print("Already liked")
                else:
                    like_button.click()
                    print("Liked the video")
                time.sleep(2)
            except Exception as e:
                print("Like button not found or could not click:", e)

        except Exception as e:
            print(f"Error processing video {idx +1}: {e}")

    # Return to target user's profile after done
    driver.get(f"https://www.tiktok.com/@{target_username}")
    print("All videos processed.")

def main():
    # User inputs
    print("TikTok Auto Like and Follow Bot")
    your_username = input("Enter your TikTok username/email/phone: ")
    your_password = getpass.getpass("Enter your TikTok password (input will be hidden): ")
    target_username = input("Enter the TikTok username you want to follow and like videos of: ")

    # Setup Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")  # Optional: run without opening browser window
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)

    try:
        logged_in = login_tiktok(driver, your_username, your_password)
        if not logged_in:
            print("Failed to login, exiting.")
            driver.quit()
            return

        follow_user(driver, target_username)
        like_all_videos(driver, target_username)

        print("Task completed! You have followed and liked videos of the user.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

