"""
CertiAce Retail Analytics — medallion pipeline (LOCAL, pure pandas).

Runs entirely on your machine. No Spark, no Fabric.
Reproduces the same Bronze -> Silver -> Gold logic as medallion_fabric.py,
reading the CSVs from ./data and writing Gold outputs to ./output.

Usage (from the repo root):
    python notebooks/medallion_local.py

Requires: pandas, pyarrow  (pip install pandas pyarrow)
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# ---------- BRONZE: load raw CSVs ----------
bronze_sales = pd.read_csv(DATA / "pos_data" / "fact_sales.csv")
bronze_date = pd.read_csv(DATA / "dim_date.csv")
bronze_stores = pd.read_csv(DATA / "dim_stores.csv")
bronze_products = pd.read_csv(DATA / "dim_products.csv")
print(f"BRONZE done: {len(bronze_sales):,} sales rows")

# ---------- SILVER: clean, de-duplicate, cast ----------
num_cols = ["Quantity", "GrossSales", "NetSales", "COGS", "GrossMargin"]
silver_sales = bronze_sales.drop_duplicates(subset=["SaleID"]).copy()
for c in num_cols:
    silver_sales[c] = pd.to_numeric(silver_sales[c], errors="coerce")
silver_sales["Quantity"] = silver_sales["Quantity"].astype("Int64")
silver_sales = silver_sales[silver_sales["NetSales"].notna()]
silver_date = bronze_date.drop_duplicates()
silver_stores = bronze_stores.drop_duplicates()
silver_products = bronze_products.drop_duplicates()
print(f"SILVER done: {len(silver_sales):,} clean sales rows")

# ---------- GOLD: star-join into an analytics-ready model ----------
dd = silver_date[["DateKey", "Year", "Quarter", "Month", "MonthName"]]
ds = silver_stores[["StoreID", "StoreName", "City", "StoreSize"]]
dp = silver_products[["ProductID", "ProductName", "Category", "SubCategory"]]
gold = (silver_sales
        .merge(dd, on="DateKey", how="left")
        .merge(ds, on="StoreID", how="left")
        .merge(dp, on="ProductID", how="left"))
gold = gold[["SaleID", "DateKey", "Year", "Quarter", "Month", "MonthName",
             "StoreID", "StoreName", "City", "StoreSize", "Region",
             "ProductID", "ProductName", "Category", "SubCategory",
             "Quantity", "GrossSales", "NetSales", "COGS", "GrossMargin",
             "SaleChannel", "PaymentMethod"]]
gold.to_parquet(OUT / "gold_sales_enriched.parquet", index=False)

agg = (gold.groupby(["Category", "Region"], as_index=False)
       .agg(TotalNetSales=("NetSales", "sum"),
            TotalGrossMargin=("GrossMargin", "sum"),
            TotalQty=("Quantity", "sum")))
agg["TotalNetSales"] = agg["TotalNetSales"].round(2)
agg["TotalGrossMargin"] = agg["TotalGrossMargin"].round(2)
agg.to_csv(OUT / "gold_sales_by_category_region.csv", index=False)

print(f"GOLD done: {len(gold):,} enriched rows | "
      f"{len(agg):,} category-region aggregates")
print(f"Outputs written to: {OUT}")
