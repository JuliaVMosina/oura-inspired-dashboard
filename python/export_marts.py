"""
Export DBT mart tables from DuckDB to CSV for Power BI import.
Run this after generate_data.py + dbt run.
Output: data/marts/*.csv
"""

import duckdb
import os

DB_PATH  = os.path.join(os.path.dirname(__file__), "..", "data", "oura.duckdb")
OUT_DIR  = os.path.join(os.path.dirname(__file__), "..", "data", "marts")
os.makedirs(OUT_DIR, exist_ok=True)

con = duckdb.connect(DB_PATH)

tables = {
    "mart_daily_scores":       "main_marts.mart_daily_scores",
    "mart_engagement_analytics": "main_marts.mart_engagement_analytics",
    "dim_users":               "main_staging.stg_users",
}

print("Exporting mart tables to CSV...")
for name, source in tables.items():
    out_path = os.path.join(OUT_DIR, f"{name}.csv")
    con.execute(f"COPY (SELECT * FROM {source}) TO '{out_path}' (HEADER, DELIMITER ',')")
    count = con.execute(f"SELECT count(*) FROM {source}").fetchone()[0]
    print(f"  {name}.csv  —  {count} rows")

con.close()
print("Done. Files saved to data/marts/")
