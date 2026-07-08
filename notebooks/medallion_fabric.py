# Fabric notebook — CertiAce Retail Analytics medallion pipeline (PySpark)
# Attach a Lakehouse as the default, then Run all.
# Reads the raw CSVs straight from the public GitHub repo (no upload needed).

import pandas as pd
from pyspark.sql import functions as F

# ---------- BRONZE: ingest raw CSVs from the public GitHub repo ----------
base = "https://raw.githubusercontent.com/erickyegon/certace-fabric-analytics/main/data"
raw = {
    "bronze_sales":    base + "/pos_data/fact_sales.csv",
    "bronze_date":     base + "/dim_date.csv",
    "bronze_stores":   base + "/dim_stores.csv",
    "bronze_products": base + "/dim_products.csv",
}
for t, u in raw.items():
    spark.createDataFrame(pd.read_csv(u)).write.mode("overwrite").format("delta").saveAsTable(t)
print("BRONZE done:", spark.table("bronze_sales").count(), "sales rows")

# ---------- SILVER: clean, de-duplicate, cast types ----------
sales = (spark.table("bronze_sales")
         .dropDuplicates(["SaleID"])
         .withColumn("Quantity", F.col("Quantity").cast("int"))
         .withColumn("GrossSales", F.col("GrossSales").cast("double"))
         .withColumn("NetSales", F.col("NetSales").cast("double"))
         .withColumn("COGS", F.col("COGS").cast("double"))
         .withColumn("GrossMargin", F.col("GrossMargin").cast("double"))
         .filter(F.col("NetSales").isNotNull()))
sales.write.mode("overwrite").format("delta").saveAsTable("silver_sales")
for d in ["date", "stores", "products"]:
    spark.table("bronze_" + d).dropDuplicates().write.mode("overwrite").format("delta").saveAsTable("silver_" + d)
print("SILVER done:", spark.table("silver_sales").count(), "clean sales rows")

# ---------- GOLD: star-join into an analytics-ready model ----------
dd = spark.table("silver_date").select("DateKey", "Year", "Quarter", "Month", "MonthName")
ds = spark.table("silver_stores").select("StoreID", "StoreName", "City", "StoreSize")
dp = spark.table("silver_products").select("ProductID", "ProductName", "Category", "SubCategory")
gold = (spark.table("silver_sales")
        .join(dd, "DateKey", "left")
        .join(ds, "StoreID", "left")
        .join(dp, "ProductID", "left")
        .select("SaleID", "DateKey", "Year", "Quarter", "Month", "MonthName",
                "StoreID", "StoreName", "City", "StoreSize", "Region",
                "ProductID", "ProductName", "Category", "SubCategory",
                "Quantity", "GrossSales", "NetSales", "COGS", "GrossMargin",
                "SaleChannel", "PaymentMethod"))
gold.write.mode("overwrite").format("delta").saveAsTable("gold_sales_enriched")
agg = (gold.groupBy("Category", "Region")
       .agg(F.round(F.sum("NetSales"), 2).alias("TotalNetSales"),
            F.round(F.sum("GrossMargin"), 2).alias("TotalGrossMargin"),
            F.sum("Quantity").alias("TotalQty")))
agg.write.mode("overwrite").format("delta").saveAsTable("gold_sales_by_category_region")
print("GOLD done:", spark.table("gold_sales_enriched").count(), "enriched rows |",
      spark.table("gold_sales_by_category_region").count(), "category-region aggregates")
