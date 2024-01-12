"""Unique School IDs"""


import pandas as pd

# Get ID's to scrape & exclude anything already completed
school_details = pd.read_excel(
    "school-location-2008-2022.xlsx", sheet_name="SchoolLocations 2008-2022"
)

unique_school_ids = pd.DataFrame({"school_ids": school_details["ACARA SML ID"].unique()})
unique_school_ids.to_csv("school_ids.csv", index=False)
