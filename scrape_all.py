"""Run scraper for all schools."""

import asyncio
import os

import pandas as pd

from scraper.naplan_scraper import naplan_scraper
from scraper.proxy_selector import read_proxy_list, select_proxy

SCHOOL_IDS = pd.read_csv("school_ids.csv")["school_ids"].to_list()
SCRAPED_IDS = [int(x.strip("_results.csv")) for x in os.listdir("results/")]
PROXIES = read_proxy_list("proxy_list.txt")


schools_to_scrape = [x for x in SCHOOL_IDS if x not in SCRAPED_IDS]


async def main():
    for school_id in schools_to_scrape[0:2]:
        proxy_info = select_proxy(PROXIES)
        await naplan_scraper(school_id, proxy_info)


if __name__ == "__main__":
    asyncio.run(main())
