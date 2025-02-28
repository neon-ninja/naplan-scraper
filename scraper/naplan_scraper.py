"""Main entry point to scrap NAPLAN results for a single school."""

import time
from typing import Dict

import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from scraper.utils import extract_naplan_results

# NAPLAN wasn't run in 2020 due to COVID
AVAILABLE_YEARS = ["2024"]
BASE_URL = "https://www.myschool.edu.au"

async def create_page():
    driver = uc.Chrome(headless=False, use_subprocess=False)
    driver.implicitly_wait(15)
    driver.get(BASE_URL)
    driver.add_cookie({"name": "TERMS_OF_USE_AGREED", "value": "1"})
    return driver

async def naplan_scraper(driver, school_id: int) -> None:
    url = f"{BASE_URL}/school/{school_id}/naplan/results/2024"
    print(url)
    driver.get(url)
    if "Page Not Found" in driver.title:
        pd.DataFrame().to_csv(f"results/{school_id}_results.csv", index=False)
        return
    table_html = driver.find_element(By.CSS_SELECTOR, "#similarSchoolsTable").get_attribute('innerHTML')
    df = extract_naplan_results(table_html, 2024)
    df.to_csv(f"results/{school_id}_results.csv", index=False)
