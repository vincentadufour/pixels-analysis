"""
Author: Vincent Dufour
Description: Main for pixels analysis.
"""

from src.data_cleaning import data_cleaning_pipeline


json_path = "data/PIXELS-BACKUP-2025-09-12T17_33_51.458262.json"

data = data_cleaning_pipeline(json_path)

print(data.head(-1))