import polars as pl

data = pl.read_csv("data/PIXELS-BACKUP-2024-10-08T22_40_14.200843.csv")

print(data.head(50))

data1 = pl.read_json("data/PIXELS-BACKUP-2025-09-12T17_33_51.458262.json")

print(f"\n{data1.head(50)}")
