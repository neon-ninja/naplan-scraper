"""Main entry point to scrap NAPLAN results for a single school."""

import time
from typing import Dict

import pandas as pd
from playwright.async_api import async_playwright

from scraper.utils import accept_tcs, extract_naplan_results, extract_raw_table_results_data

# NAPLAN wasn't run in 2020 due to COVID
AVAILABLE_YEARS = ["2014", "2015", "2016", "2017", "2018", "2019", "2021", "2022"]
BASE_URL = "https://www.myschool.edu.au"


async def naplan_scraper(school_id: int, proxy_details: Dict[str, str]) -> None:
    async with async_playwright() as pw:
        print(f"Attempting: {school_id}")
        browser = await pw.chromium.launch(
            headless=False,
            proxy={
                "server": proxy_details["server"],
                "username": proxy_details["username"],
                "password": proxy_details["password"],
            },
        )

        page = await browser.new_page()

        # Navigate to website & accept T&C's
        await page.goto(BASE_URL)
        time.sleep(1.5)
        print("Accepting T&C's...")
        await accept_tcs(page)

        print("Scraping results...")
        results = []
        for year_of_interest in AVAILABLE_YEARS:
            print(f"Scraping results for {year_of_interest}...")
            time.sleep(1.5)

            # Navigate to school year
            school_url = f"{BASE_URL}/school/{school_id}/naplan/results"
            await page.goto(f"{school_url}/{year_of_interest}")

            # Extract results table HTML
            table_html = await extract_raw_table_results_data(page)

            # Results for year
            results.append(extract_naplan_results(table_html, year_of_interest))

        results_df = pd.concat(results)
        results_df.to_csv(f"results/{school_id}_results.csv", index=False)
        print(f"Successfully scraped: {school_id}")
        await browser.close()
