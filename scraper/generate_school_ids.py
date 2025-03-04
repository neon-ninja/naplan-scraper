"""Unique School IDs"""


import pandas as pd

# Get ID's to scrape & exclude anything already completed
df = pd.read_excel("School Location 2024.xlsx", sheet_name="SchoolLocations 2024")

print(df.State.value_counts())
df = df[df.State == "WA"]
df = pd.DataFrame({"school_ids": df["ACARA SML ID"].unique()})
df.to_csv("school_ids.csv", index=False)
