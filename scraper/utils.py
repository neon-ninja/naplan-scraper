"""Utilities to aid scraping."""

from io import StringIO

import boto3
import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import Page


async def extract_raw_table_results_data(page: Page):
    """Retrieve the NAPLAN results table

    Args:
        page (_type_): School Results page, eg:
            https://www.myschool.edu.au/school/44461/naplan/results

    Returns:
        _type_: _description_
    """
    table_html = await page.inner_html("#similarSchoolsTable")
    return table_html


async def accept_tcs(page: Page) -> None:
    """Accepts T&C's

    Args:
        page (_type_): _description_
    """
    try:
        # Click the "I Accept Box"
        await page.get_by_role("checkbox").check()

        # Click the "Accept" button
        await page.get_by_role("button", name="Accept").click()

    except Exception as ex:
        print("Error in accepting T&C's")
        print(ex)


def extract_naplan_results(raw_table_html: str, calendar_year: int) -> pd.DataFrame:
    """Parses the raw NAPLAN results HTML & returns a cleaned dataframe.

    Args:
        raw_table_html (_type_): HTML block containing the naplan results
        calendar_year (int): Year the results were captured

    Returns:
        pd.DataFrame: DataFrame with columns:
            year_level: Grades 3,5,7 or 9
            avg: Average result for the year
            err_low: lower bound
            err_high: upper bound
            results_year: year the results were captured
            domain: The area being tested, eg Numeracy, Reading, etc
            test_type: Either online or paper
    """
    soup = BeautifulSoup(raw_table_html, "html.parser")

    # Find the table with the specified ID and class
    table = soup.find("table", {"id": "similarSchoolsTable", "class": "naplan-result-table"})  # noqa

    # Get Table Headers
    table_headers = [x.text.strip() for x in soup.find_all("th") if x.text.strip() != ""]

    tbody = soup.find("tbody")

    results = []
    test_type = []

    for row in tbody.find_all("tr"):
        element_class = row.get("class")
        # print(element_class)

        if element_class is None:
            year_level = row.find("td").get_text(strip=True)

        elif "selected-school-row" in element_class:
            # a[1].find('span', class_='err').get_text(strip=True)
            avg_value = row.find("span", class_="avg").get_text(strip=True)

            if avg_value in ["Online", "Paper"]:
                test_type.append(avg_value)
                continue

            err_value = row.find("span", class_="err").get_text(strip=True)

            # Split the 'err' value into low and high
            err_low, err_high = map(int, err_value.split("-"))

            # Create a dictionary
            result_dict = {
                "year_level": year_level,
                "avg": avg_value,
                "err_low": err_low,
                "err_high": err_high,
                "results_year": calendar_year,
            }

            results.append(result_dict)

    df = pd.DataFrame(results)

    # The data is in row base, rather than column based format
    # Thus, we need to repeat the table headers for each year level
    required_multiples = len(df) // len(table_headers)
    df["domain"] = table_headers * required_multiples
    if len(test_type) == df.shape[0]:
        df["test_type"] = test_type
    return df


def save_results_to_s3(results: pd.DataFrame, school_id: int) -> None:
    """Write scraped results to S3

    Args:
        results (pd.DataFrame): Scraped naplan results
        school_id (int): School SMLID
    """
    # Config
    # Should both probs be from env-vars but ceebs
    bucket_name = "naplan"
    file_key = f"{school_id}_results.csv"

    # Store file in memory buffer rather than writing to disk
    csv_buffer = StringIO()
    results.to_csv(csv_buffer, index=False)

    # Setup Session & save file
    s3_client = boto3.client("s3")
    s3_client.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=file_key)
