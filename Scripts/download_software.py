#!/usr/bin/env python3
"""
Automated Software Download Script using Playwright

Usage:
    python download_software.py

Environment variables:
    DOWNLOAD_DIR - Download destination (default: /downloads)
"""

import os
import sys
from datetime import datetime
from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError,
)


# =============================================================================
# CONFIGURATION
# =============================================================================

LOGIN_URL = "https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+Workstation+Pro"

# Credentials
USERNAME = "weehongkane@gmail.com"
PASSWORD = "MyselF900223+"

# CSS Selectors - Login
SELECTOR_USERNAME_FIELD = "#usernameInput"
SELECTOR_PASSWORD_FIELD = "#passwordInput"
SELECTOR_NEXT_BUTTON = ".primary-button"

# CSS Selectors - Navigation & Download
SELECTOR_MY_DOWNLOADS = ".ecx-left-nav > nav:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li:nth-child(4) > a:nth-child(1) > div:nth-child(3)"
SELECTOR_HERE_LINK = "a[href='/group/ecx/free-downloads']"
SELECTOR_COOKIE_ALLOW = "button:has-text('Allow All')"
SELECTOR_SEARCH_INPUT = ".brcm-mobile-flex > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)"
SELECTOR_SHOW_RESULT_BTN = ".btn-sm"
SELECTOR_WORKSTATION_PRO = ".p-3"
SELECTOR_EXPAND_VERSION = "div.panel:nth-child(1) > button:nth-child(1) > div:nth-child(1) > div:nth-child(1)"
SELECTOR_DOWNLOAD_ICON = ".btn-link"

# Download settings - /downloads is the Docker mount point
DOWNLOAD_DIR = "/downloads"

# Timeouts (in milliseconds)
DEFAULT_TIMEOUT = 30000  # 30 seconds


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def print_status(message: str, is_error: bool = False) -> None:
    """Print a timestamped status message to console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = "ERROR" if is_error else "INFO"
    print(f"[{timestamp}] {prefix}: {message}")


# =============================================================================
# MAIN
# =============================================================================


def run_automation():
    """Main automation function."""
    print_status("Starting automation script...")
    print_status(f"Download directory: {DOWNLOAD_DIR}")

    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        context.set_default_timeout(DEFAULT_TIMEOUT)
        page = context.new_page()

        try:
            # Navigate to login page
            print_status(f"Navigating to: {LOGIN_URL}")
            page.goto(LOGIN_URL)
            page.wait_for_load_state("networkidle")

            print_status("Page loaded successfully!")
            print_status(f"Current URL: {page.url}")

            # Fill in username
            print_status("Filling in username...")
            page.locator(SELECTOR_USERNAME_FIELD).wait_for(state="visible")
            page.locator(SELECTOR_USERNAME_FIELD).fill(USERNAME)
            print_status("Username entered")

            # Click next button
            print_status("Clicking next...")
            page.locator(SELECTOR_NEXT_BUTTON).click()

            # Wait for password field to appear
            print_status("Waiting for password field...")
            page.locator(SELECTOR_PASSWORD_FIELD).wait_for(state="visible")

            # Fill in password
            print_status("Filling in password...")
            page.locator(SELECTOR_PASSWORD_FIELD).fill(PASSWORD)
            print_status("Password entered")

            # Click Sign In button to submit
            print_status("Clicking Sign In...")
            page.locator(SELECTOR_NEXT_BUTTON).click()

            # Wait for login to complete
            page.wait_for_timeout(5000)
            print_status(f"Current URL after Sign In: {page.url}")

            # Verify we're no longer on the login page
            if "signin" in page.url:
                print_status("Still on login page - login may have failed", is_error=True)
                return False

            print_status("Login successful!")
            print_status(f"Current URL: {page.url}")

            # Dismiss cookies popup if present
            try:
                cookie_btn = page.locator(SELECTOR_COOKIE_ALLOW)
                if cookie_btn.is_visible(timeout=3000):
                    print_status("Dismissing cookies popup...")
                    cookie_btn.click()
                    page.wait_for_timeout(1000)
            except Exception:
                pass  # Cookie popup might not be present

            # ========== NAVIGATION TO DOWNLOAD ==========

            # Click "My Downloads" in sidebar
            print_status("Clicking 'My Downloads'...")
            page.locator(SELECTOR_MY_DOWNLOADS).wait_for(state="visible")
            page.locator(SELECTOR_MY_DOWNLOADS).click()
            page.wait_for_load_state("networkidle")
            print_status(f"Current URL: {page.url}")

            # Click "HERE" hyperlink
            print_status("Clicking 'HERE' link...")
            page.locator(SELECTOR_HERE_LINK).wait_for(state="visible")
            page.locator(SELECTOR_HERE_LINK).click()
            page.wait_for_load_state("networkidle")
            print_status(f"Current URL: {page.url}")

            # Enter "VMware Workstation" in search input
            print_status("Entering search term: VMware Workstation...")
            page.locator(SELECTOR_SEARCH_INPUT).wait_for(state="visible")
            page.locator(SELECTOR_SEARCH_INPUT).fill("VMware Workstation")

            # Click "Show Result" button
            print_status("Clicking 'Show Result'...")
            page.locator(SELECTOR_SHOW_RESULT_BTN).click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(3000)  # Wait for results to load

            # Click on VMware Workstation Pro
            print_status("Clicking 'VMware Workstation Pro'...")
            page.locator(SELECTOR_WORKSTATION_PRO).wait_for(state="visible")
            page.locator(SELECTOR_WORKSTATION_PRO).click()
            page.wait_for_load_state("networkidle")
            print_status(f"Current URL: {page.url}")

            # Dismiss cookies popup if present again
            try:
                cookie_btn = page.locator(SELECTOR_COOKIE_ALLOW)
                if cookie_btn.is_visible(timeout=2000):
                    print_status("Dismissing cookies popup...")
                    cookie_btn.click()
                    page.wait_for_timeout(1000)
            except Exception:
                pass

            # Click to expand the latest version
            print_status("Expanding latest version...")
            page.locator(SELECTOR_EXPAND_VERSION).wait_for(state="visible")
            page.locator(SELECTOR_EXPAND_VERSION).click()
            page.wait_for_timeout(2000)  # Wait for expansion animation

            # Click on the 25H2 release link to go to download page
            print_status("Clicking on 25H2 release...")
            page.locator("a:has-text('25H2')").first.wait_for(state="visible")
            page.locator("a:has-text('25H2')").first.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            print_status(f"Current URL: {page.url}")

            # Click download icon button
            print_status("Clicking download button...")
            page.locator(SELECTOR_DOWNLOAD_ICON).wait_for(state="visible")

            # Setup download handling
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)

            with page.expect_download(timeout=300000) as download_info:  # 5 min timeout
                page.locator(SELECTOR_DOWNLOAD_ICON).click()

            download = download_info.value
            print_status(f"Download started: {download.suggested_filename}")

            # Save as fixed filename (overwrites existing)
            filepath = os.path.join(DOWNLOAD_DIR, "vmware-workstation.exe")

            print_status("Waiting for download to complete...")
            download.save_as(filepath)

            print_status(f"Download completed: {filepath}")

            return True

        except PlaywrightTimeoutError as e:
            print_status(f"Timeout error: {e}", is_error=True)
            return False
        except PlaywrightError as e:
            print_status(f"Playwright error: {e}", is_error=True)
            return False
        except Exception as e:
            print_status(f"Unexpected error: {e}", is_error=True)
            import traceback

            traceback.print_exc()
            return False
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    success = run_automation()
    sys.exit(0 if success else 1)
