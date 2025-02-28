#!/usr/bin/env python3

"""Run scraper for all schools."""

import asyncio
import os

import pandas as pd
from tqdm.auto import tqdm

from scraper.naplan_scraper import create_page, naplan_scraper

SCHOOL_IDS = pd.read_csv("school_ids.csv")["school_ids"].to_list()
os.makedirs("results", exist_ok=True)
SCRAPED_IDS = [int(x.strip("_results.csv")) for x in os.listdir("results/")]

schools_to_scrape = [x for x in SCHOOL_IDS if x not in SCRAPED_IDS]

async def main():
    page = await create_page()
    for school_id in tqdm(schools_to_scrape):
        await naplan_scraper(page, school_id)

if __name__ == "__main__":
    asyncio.run(main())
