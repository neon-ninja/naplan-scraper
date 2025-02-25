"""Main entry point to scrap NAPLAN results for a single school."""

import time
from typing import Dict

import pandas as pd
#from playwright.async_api import async_playwright
from patchright.async_api import async_playwright, Page

from scraper.utils import extract_naplan_results, extract_raw_table_results_data

# NAPLAN wasn't run in 2020 due to COVID
AVAILABLE_YEARS = ["2024"]
BASE_URL = "https://www.myschool.edu.au"

async def create_page(proxy_details: Dict[str, str]):
    playwright = await async_playwright().start()
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir="user_data",
        channel="chrome",
        headless=False,
        no_viewport=True,
    )
    await context.add_cookies([{'name': 'TERMS_OF_USE_AGREED', 'value': '1', 'url': BASE_URL}])
    page = await context.new_page()
    return page

async def naplan_scraper(page: Page, school_id: int) -> None:
    await page.goto(f"{BASE_URL}/school/{school_id}/naplan/results/2024")
    table_html = await extract_raw_table_results_data(page)
    df = extract_naplan_results(table_html, 2024)
    df.to_csv(f"results/{school_id}_results.csv", index=False)
