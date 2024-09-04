import pandas as pd
import nfl_data_py as nfl
import os

chap_1_file = "./data/pbp_py_chap_2023.csv"

if os.path.isfile(chap_1_file):
    pbp_py = pd.read_csv(chap_1_file, low_memory=False)
else:
    pbp_py = nfl.import_pbp_data([2023])
    pbp_py.to_csv(chap_1_file)

## filter out passing data
filter_crit = 'play_type == "pass" & air_yards.notnull()'
pbp_py_p = (
    pbp_py.query(filter_crit)
    .groupby(["passer_id", "passer"])
    .agg({"air_yards": ["count", "mean"]})
)

## format and print data for passing plays
pbp_py_p.columns = list(map("_".join, pbp_py_p.columns.values))
sort_crit = "air_yards_count > 100"
print(
    pbp_py_p.query(sort_crit)
    .sort_values(by="air_yards_mean", ascending=[False])
    .to_string()
)