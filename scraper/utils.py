"""Utilities to aid scraping."""


import pandas as pd
from bs4 import BeautifulSoup

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
    sim_avg = []

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
        
        elif "sim-all-row" in element_class:
            sim_avg.append(row.find("span", class_="sim-avg").get_text(strip=True))

    df = pd.DataFrame(results)

    # The data is in row base, rather than column based format
    # Thus, we need to repeat the table headers for each year level
    required_multiples = len(df) // len(table_headers)
    #df["domain"] = table_headers * required_multiples
    if len(test_type) == df.shape[0]:
        df["test_type"] = test_type
    if len(sim_avg) == df.shape[0]:
        df["sim_avg"] = sim_avg
    return df

if __name__ == "__main__":
    with open("sample.html", "r") as f:
        raw_html = f.read()
        df = extract_naplan_results(raw_html, 2024)
        print(df)