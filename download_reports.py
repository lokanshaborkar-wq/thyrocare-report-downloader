import os
import pandas as pd
from playwright.sync_api import sync_playwright

EXCEL_FILE = "TOYO Report links.xlsx"
DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

df = pd.read_excel(EXCEL_FILE)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    input("Press ENTER after the browser opens...")

    for index, row in df.iterrows():
        print(f"Downloading {index+1}/{len(df)}")

        page.goto(row["Reports links"])

        page.wait_for_selector("button:has-text('Download Report')")

        with page.expect_download() as download_info:
            page.locator("button:has-text('Download Report')").click()

        download = download_info.value
        download.save_as(
            os.path.join(DOWNLOAD_DIR, download.suggested_filename)
        )

        print("Downloaded:", download.suggested_filename)

    browser.close()

print("Completed")
