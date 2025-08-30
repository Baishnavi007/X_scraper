import os
import time
import socket
import django
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from datetime import datetime

# -----------------------------
# Django + Env Setup
# -----------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "X_scraper.settings")
django.setup()

from trends_scraper.models import TrendRun  # Django ORM

load_dotenv()
X_EMAIL = os.getenv("X_EMAIL")
X_USERNAME = os.getenv("X_USERNAME")
X_PASSWORD = os.getenv("X_PASSWORD")


# -----------------------------
# Selenium Login Function
# -----------------------------
def login_to_x(proxy: str = None):
    options = Options()
    options.add_argument("--headless=new")  # Headless mode for server deployment
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1400,900")

    if proxy:
        options.add_argument(f"--proxy-server={proxy}")
        print(f"🌐 Using Proxy: {proxy}")

    driver = webdriver.Chrome(options=options)
    driver.get("https://x.com/login")

    wait = WebDriverWait(driver, 10)

    # Enter email
    wait.until(EC.presence_of_element_located((By.NAME, "text"))).send_keys(X_EMAIL, Keys.RETURN)

    # Enter username only if asked
    try:
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        username_field.send_keys(X_USERNAME, Keys.RETURN)
    except:
        print("⚠ Username step skipped")

    # Enter password
    wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(X_PASSWORD, Keys.RETURN)

    # Wait for login to complete
    wait.until(EC.url_contains("home"))
    print("✅ Logged in successfully!")
    return driver


# -----------------------------
# Fetch Top Trends
# -----------------------------
def fetch_top_trends(driver):
    driver.get("https://x.com/explore")
    wait = WebDriverWait(driver, 10)

    # Wait until trend elements load
    trend_elements = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="cellInnerDiv"]'))
    )

    texts = [t.text for t in trend_elements if t.text.strip()]
    trend_names = [t.split("\n")[1] if "\n" in t else t for t in texts]

    return trend_names[:5]


# -----------------------------
# Save to DB
# -----------------------------
def save_to_db(trends, ip_address="Unknown"):
    # Ensure always 5 trends
    while len(trends) < 5:
        trends.append("")

    TrendRun.objects.create(
        trend1=trends[0],
        trend2=trends[1],
        trend3=trends[2],
        trend4=trends[3],
        trend5=trends[4],
        scraped_at=datetime.utcnow(),
        ip_address=ip_address
    )
    print("✅ Data inserted into DB!")


# -----------------------------
# Main Runner
# -----------------------------
def main(proxy: str = None):
    driver = None
    try:
        driver = login_to_x(proxy)
        trends = fetch_top_trends(driver)
        print("🔥 Top 5 Trends:", trends)

        # Get public IP
        try:
            ip_address = requests.get("https://api.ipify.org", timeout=5).text
        except:
            ip_address = "Unknown"

        save_to_db(trends, ip_address=ip_address)
        return trends

    except Exception as e:
        print(f"❌ Scraper failed: {e}")
        return []

    finally:
        if driver:
            driver.quit()
