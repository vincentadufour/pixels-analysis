"""Description: Main for pixels analysis."""

import polars as pl
import datetime as dt

from src.analysis import compare_average_score_with_term
from src.data_cleaning import data_cleaning_driver
from src.plots import plot_all_graphs


json_path = "data/PIXELS-BACKUP-2025-09-12T17_33_51.458262.json"

data = data_cleaning_driver(json_path)

print(data.head(-15))

# TODO: React? AWS? User upload? Local cached json/dataframe data?

data_pd = data.to_pandas()
plot_all_graphs(data_pd)    


search_term = "watch"
compare_average_score_with_term(data_pd, search_term, 5)