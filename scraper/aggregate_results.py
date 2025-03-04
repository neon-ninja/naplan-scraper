#!/usr/bin/env python3

import pandas as pd
from tqdm.auto import tqdm
tqdm.pandas()
import geopandas

df = pd.read_excel("School Location 2024.xlsx", sheet_name="SchoolLocations 2024")
df = df[df.State == "WA"]

def get_results(school_id):
  try:
    school_df = pd.read_csv(f"results/{school_id}_results.csv")
    return school_df.avg.mean(), school_df.sim_avg.mean()
  except Exception as e:
    return None, None

df["school_avg"], df["school_sim_avg"] = zip(*df["ACARA SML ID"].progress_apply(get_results))
df["diff"] = df["school_avg"] - df["school_sim_avg"]

df.to_csv("WA_schools.csv", index=False)

df = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326"
)

df["link"] = df["ACARA SML ID"].apply(lambda x: f'<a href="https://www.myschool.edu.au/school/{x}/naplan/results/2024">Link</a>')

m = df.explore("diff", legend=True, cmap="jet_r", title="WA School NAPLAN Results", marker_type="circle", marker_kwds={"fill": True, "radius": 100}, style_kwds={"fillOpacity": 0.8}, tiles="CartoDB positron", popup=True)
m.save("WA_schools.html")