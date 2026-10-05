# CertiAce Retail Analytics — Microsoft Fabric End-to-End Portfolio Project

> **A production-grade Microsoft Fabric implementation covering every DP-600 exam domain:**
> security & governance · medallion architecture · data pipelines · semantic modeling · DAX · KQL · deployment lifecycle

[![Microsoft Fabric](https://img.shields.io/badge/Microsoft%20Fabric-F128%20Capacity-0078D4?style=flat&logo=microsoft)](https://learn.microsoft.com/en-us/fabric/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Semantic%20Model-F2C811?style=flat&logo=powerbi)](https://powerbi.microsoft.com/)
[![KQL](https://img.shields.io/badge/KQL-Real--Time%20Analytics-00BCF2?style=flat)](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/)
[![DAX](https://img.shields.io/badge/DAX-Advanced%20Measures-FF6B35?style=flat)](https://learn.microsoft.com/en-us/dax/)

---

## 📋 Business Scenario

**CertiAce** operates a global retail chain with **2,000 stores across North America and Europe**, managing sales, inventory, and supply chain logistics data.

### Problem Statements Solved

| # | Problem | Solution Implemented |
|---|---------|---------------------|
| 1 | Individual user access grants — inconsistent permissions & security risks | Security group–based workspace access + RLS/OLS on semantic models |
| 2 | Manual artifact promotion across environments — inconsistent deployments | Automated deployment pipelines: Dev → Test → Prod |
| 3 | Duplicate supplier records + missing delivery times — inaccurate reports | Silver layer deduplication + null handling + data quality logging |
| 4 | Slow dashboards due to inefficient DAX + no incremental refresh | Direct Lake mode + incremental refresh + optimized DAX with variables |
| 5 | SAP CSV failures due to inconsistent file naming + late arrivals | Parameterized pipeline with error handling, retry logic, audit logging |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Microsoft Fabric F128 Capacity               │
│                         'RetailCap'                             │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ ws_retail_dev│  │ws_retail_test│  │   ws_retail_prod     │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │    Deployment Pipeline                  │             │
│         └──────────────────────────────────────────             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ws_experiment_sandbox (Data Scientists)      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

Data Flow:
                                                                   
  [Azure SQL / POS]  ──►  BRONZE Lakehouse  ──►  SILVER Lakehouse  ──►  GOLD Warehouse
  [SAP CSV Exports]        (Raw Ingestion)        (Cleansed/Enriched)    (Star Schema)
                                                                              │
                                                                    [Semantic Model]
                                                                              │
                                                                    [Power BI Reports]
```

---

## 📁 Repository Structure

```
certace-fabric-analytics/
│
├── 📂 data/                                # 555K rows across 8 datasets (see below)
│   ├── pos_data/fact_sales.csv             # 500K POS transactions
│   ├── sap_exports/fact_supplier_deliveries.csv  # 40K rows, intentional DQ issues
│   ├── fact_inventory.csv
│   ├── dim_stores.csv / dim_products.csv / dim_suppliers.csv / dim_date.csv
│   └── security_groups.csv                 # 18 security group definitions
│
├── 📂 notebooks/                           # End-to-end medallion pipeline (runnable)
│   ├── medallion_fabric.py                 # Full Bronze→Silver→Gold, PySpark, runs in any Fabric Lakehouse
│   │                                        # (pulls the raw CSVs directly from this repo's GitHub URLs)
│   ├── medallion_local.py                  # Same Bronze→Silver→Gold logic, pandas-only — runs on any machine
│   ├── make_charts.py                      # Renders the charts below from the Gold layer
│   └── README.md                           # How to run each script
│
├── 📂 02_bronze/notebooks/                 # Reference notebook: POS ingestion with audit columns
├── 📂 03_silver/notebooks/                 # Reference notebook: supplier dedup logic
│
├── 📂 06_semantic_model/measures/          # DAX measure library (sales, inventory, supplier KPIs)
├── 📂 07_security/rls_definitions.md       # Dynamic RLS (per-region) + OLS (hidden pricing columns)
├── 📂 08_kql/                              # KQL queries for Eventhouse: real-time sales, delivery anomalies
├── 📂 09_deployment/pre_deployment_checks.md  # Dev→Test→Prod promotion checklist
│
├── 📂 docs/images/                         # Gold-layer charts (category, region, monthly trend)
├── 📂 output/gold_sales_by_category_region.csv
└── README.md
```

> **Note on scope:** `notebooks/medallion_fabric.py` and `medallion_local.py` are the working,
> runnable implementation of the full Bronze → Silver → Gold pipeline. The numbered folders
> (`02_bronze`, `03_silver`, `06_semantic_model`, etc.) hold focused reference artifacts —
> DAX measures, RLS/OLS definitions, KQL queries, deployment checklist — that map directly to
> pieces of that pipeline rather than a separate parallel build.

---

## 📊 Dataset Summary

| Dataset | Rows | Layer | Description |
|---------|------|-------|-------------|
| `fact_sales.csv` | 500,000 | Bronze/Silver/Gold | POS transactions 2022–2024, 2,000 stores |
| `fact_supplier_deliveries.csv` | 40,000 | Bronze/Silver/Gold | SAP exports with DQ issues embedded |
| `fact_inventory.csv` | 12,000 | Bronze/Silver/Gold | Daily stock snapshot with reorder alerts |
| `dim_stores.csv` | 1,685 | All layers | Store master with region, country, size |
| `dim_products.csv` | 268 | All layers | Product catalog with cost, price, margin |
| `dim_suppliers.csv` | 58 | All layers | Supplier master with **8 intentional duplicates** |
| `dim_date.csv` | 1,096 | All layers | Date dimension 2022–2024 with fiscal calendar |
| `security_groups.csv` | 18 | Reference | Security group → Region → RLS mapping |

**Total: 555,107 rows** across 8 datasets

### Intentional Data Quality Issues (for Silver layer exercise)
- **Duplicate suppliers:** 8 records duplicated with case variations (`"Acme Corp"` vs `"ACME CORP"`)
- **Missing delivery dates:** ~5% of `ActualDeliveryDate` values are NULL
- **Inconsistent file naming:** ~1.2% of SAP exports use `dd-MM-yyyy.CSV` instead of `yyyyMMdd.csv`
- **Zero stock scenarios:** Some inventory rows trigger `ReorderStatus = "Reorder Required"`
- **Late deliveries:** Mix of On Time / Late / Significantly Late delivery statuses

---

## 🔧 Implementation Details

### 1. Security & Governance

#### Workspace Access Matrix

| Security Group | ws_dev | ws_test | ws_prod | ws_sandbox |
|---|---|---|---|---|
| SG_FabricAdmins | Admin | Admin | Admin | Admin |
| SG_DataEngineers | Contributor | Contributor | Viewer | Contributor |
| SG_Analysts | — | Viewer | Viewer | — |
| SG_DataScientists | — | — | Viewer | Contributor |
| SG_RegMgr_* | — | — | Viewer (RLS) | — |
| SG_Executives | — | — | Viewer | — |

#### Row-Level Security (DAX)

```dax
-- Regional Manager RLS filter on semantic model
[Region] = USERPRINCIPALNAME() -- mapped via security group lookup

-- Implementation using CUSTOMDATA()
RegionalFilter =
VAR CurrentUser = USERPRINCIPALNAME()
VAR UserRegion = LOOKUPVALUE(SecurityGroups[Region], SecurityGroups[UserEmail], CurrentUser)
RETURN IF(UserRegion = "ALL", TRUE(), [Region] = UserRegion)
```

#### Object-Level Security (Supplier Pricing)
```
-- Supplier pricing columns hidden from SG_Analysts:
-- DimSuppliers[ContractValue]
-- DimSuppliers[PricingCategory]  
-- DimSuppliers[UnitCost]
-- Applied via XMLA endpoint / Tabular Editor
```

---

### 2. Bronze Layer — Raw Ingestion

#### POS Sales Pipeline (PySpark)
```python
# ingest_pos_sales.ipynb — Bronze ingestion
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit, input_file_name

spark = SparkSession.builder.getOrCreate()

df_raw = (spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("Files/pos_data/fact_sales.csv"))

# Add audit columns
df_bronze = (df_raw
    .withColumn("_ingested_at", current_timestamp())
    .withColumn("_source_file", input_file_name())
    .withColumn("_layer", lit("bronze")))

# Write to Bronze Lakehouse as Delta
(df_bronze.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", True)
    .saveAsTable("bronze_lakehouse.fact_sales_raw"))

print(f"Ingested {df_bronze.count():,} rows to Bronze")
```

#### SAP Delivery Pipeline — Error Handling
```python
# ingest_sap_deliveries.ipynb — with file naming validation
import re
from pyspark.sql.functions import when, col, regexp_extract

VALID_PATTERN = r"SAP_EXPORT_\d{8}\.csv"

df_raw = spark.read.option("header", True).csv("Files/sap_exports/")

# Flag invalid file names
df_with_audit = df_raw.withColumn(
    "_file_name_valid",
    when(col("FileSource").rlike(VALID_PATTERN), True).otherwise(False)
).withColumn("_ingested_at", current_timestamp())

# Separate valid and quarantined records
df_valid = df_with_audit.filter(col("_file_name_valid") == True)
df_quarantine = df_with_audit.filter(col("_file_name_valid") == False)

df_valid.write.format("delta").mode("append").saveAsTable("bronze_lakehouse.fact_deliveries_raw")
df_quarantine.write.format("delta").mode("append").saveAsTable("bronze_lakehouse.fact_deliveries_quarantine")

print(f"✅ Valid: {df_valid.count():,} | ⚠️ Quarantined: {df_quarantine.count():,}")
```

---

### 3. Silver Layer — Cleansing & Enrichment

#### Supplier Deduplication
```python
# clean_suppliers.ipynb
from pyspark.sql.functions import upper, trim, row_number
from pyspark.sql.window import Window

df_sup = spark.table("bronze_lakehouse.dim_suppliers_raw")

# Normalize for dedup comparison
df_normalized = df_sup.withColumn("_name_normalized", upper(trim(col("SupplierName"))))

# Keep most recent record per normalized name
window = Window.partitionBy("_name_normalized").orderBy(col("SupplierID").desc())
df_deduped = (df_normalized
    .withColumn("_rank", row_number().over(window))
    .filter(col("_rank") == 1)
    .drop("_rank", "_name_normalized"))

removed = df_sup.count() - df_deduped.count()
print(f"Removed {removed} duplicate supplier records")

df_deduped.write.format("delta").mode("overwrite").saveAsTable("silver_lakehouse.dim_suppliers")
```

#### Sales Enrichment — Gross Margin & Calculated Fields
```python
# transform_sales.ipynb
from pyspark.sql.functions import col, round as spark_round, when

df_sales = spark.table("bronze_lakehouse.fact_sales_raw")
df_products = spark.table("silver_lakehouse.dim_products")

df_enriched = (df_sales
    .join(df_products.select("ProductID","UnitCost"), "ProductID", "left")
    .withColumn("GrossMargin", spark_round(col("NetSales") - (col("UnitCost") * col("Quantity")), 2))
    .withColumn("GrossMarginPct", spark_round(col("GrossMargin") / col("NetSales") * 100, 2))
    .withColumn("IsHighMargin", when(col("GrossMarginPct") >= 40, True).otherwise(False))
    .withColumn("SaleQuarter",
        when(col("DateKey").cast("string").substr(5,2).cast("int").between(1,3), "Q1")
        .when(col("DateKey").cast("string").substr(5,2).cast("int").between(4,6), "Q2")
        .when(col("DateKey").cast("string").substr(5,2).cast("int").between(7,9), "Q3")
        .otherwise("Q4")))

df_enriched.write.format("delta").mode("overwrite").saveAsTable("silver_lakehouse.fact_sales")
```

---

### 4. Gold Layer — Star Schema

```sql
-- build_fact_sales_gold.sql (T-SQL in Fabric Warehouse)
CREATE TABLE gold_warehouse.FactSales AS
SELECT
    s.SaleID,
    s.DateKey,
    s.StoreID,
    s.ProductID,
    s.Quantity,
    s.GrossSales,
    s.NetSales,
    s.COGS,
    s.GrossMargin,
    s.GrossMarginPct,
    s.DiscountPct,
    s.SaleChannel,
    s.PaymentMethod,
    st.Region,
    st.Country,
    p.Category,
    p.SubCategory
FROM silver_lakehouse.fact_sales s
LEFT JOIN silver_lakehouse.dim_stores st ON s.StoreID = st.StoreID
LEFT JOIN silver_lakehouse.dim_products p ON s.ProductID = p.ProductID
WHERE st.IsActive = 1;
```

---

### 5. DAX Measures — Semantic Model

```dax
-- ============================================
-- CORE SALES MEASURES
-- ============================================

Total Net Sales = SUM(FactSales[NetSales])

Total Gross Margin = SUM(FactSales[GrossMargin])

Gross Margin % = 
DIVIDE([Total Gross Margin], [Total Net Sales], 0)

Units Sold = SUM(FactSales[Quantity])

Avg Transaction Value = 
DIVIDE([Total Net Sales], DISTINCTCOUNT(FactSales[SaleID]), 0)

-- ============================================
-- TIME INTELLIGENCE
-- ============================================

Sales MTD = 
CALCULATE([Total Net Sales], DATESMTD(DimDate[Date]))

Sales QTD = 
CALCULATE([Total Net Sales], DATESQTD(DimDate[Date]))

Sales YTD = 
CALCULATE([Total Net Sales], DATESYTD(DimDate[Date]))

Sales PY = 
CALCULATE([Total Net Sales], PREVIOUSYEAR(DimDate[Date]))

Sales YoY Growth = 
VAR CurrentSales = [Total Net Sales]
VAR PriorSales = [Sales PY]
RETURN
DIVIDE(CurrentSales - PriorSales, PriorSales, BLANK())

Sales YoY Growth % = 
FORMAT([Sales YoY Growth], "0.0%")

-- ============================================
-- INVENTORY KPIs
-- ============================================

Out of Stock Count = 
CALCULATE(COUNTROWS(FactInventory), FactInventory[StockOnHand] = 0)

Out of Stock Rate = 
DIVIDE([Out of Stock Count], COUNTROWS(FactInventory), 0)

Reorder Required Count = 
CALCULATE(
    COUNTROWS(FactInventory),
    FactInventory[ReorderStatus] = "Reorder Required"
)

Avg Days of Supply = 
AVERAGE(FactInventory[DaysOfSupply])

-- ============================================
-- SUPPLIER DELIVERY KPIs
-- ============================================

On Time Delivery Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(FactDeliveries), FactDeliveries[DeliveryStatus] = "On Time"),
    COUNTROWS(FactDeliveries),
    0
)

Avg Delivery Delay Days = 
AVERAGEX(
    FILTER(FactDeliveries, FactDeliveries[DeliveryStatus] <> "On Time"),
    DATEDIFF(FactDeliveries[ExpectedDeliveryDate], FactDeliveries[ActualDeliveryDate], DAY)
)

Missing Delivery Dates = 
CALCULATE(COUNTROWS(FactDeliveries), ISBLANK(FactDeliveries[ActualDeliveryDate]))

-- ============================================
-- REGIONAL PERFORMANCE (respects RLS)
-- ============================================

Region Sales % of Total = 
DIVIDE(
    [Total Net Sales],
    CALCULATE([Total Net Sales], ALLEXCEPT(DimStores, DimStores[Region])),
    0
)

-- ============================================
-- RUNNING TOTAL (WINDOW function)
-- ============================================

Running Sales Total = 
SUMX(
    WINDOW(1, ABS, 0, REL, ORDERBY(DimDate[Date], ASC)),
    [Total Net Sales]
)
```

---

### 6. KQL — Real-Time Analytics (Eventhouse)

```kql
// realtime_sales_monitor.kql
// Live sales monitoring — last 15 minutes
SalesStream
| where ingestion_time() > ago(15m)
| extend SaleAge = now() - ingestion_time()
| summarize 
    TotalSales = sum(NetSales),
    TxCount = count(),
    AvgTxValue = avg(NetSales)
  by bin(ingestion_time(), 1m), Region
| order by ingestion_time() desc

// delivery_anomaly_detection.kql
// Flag late deliveries in real time
SupplierDeliveries
| where ActualDeliveryDate > ExpectedDeliveryDate
| extend DelayDays = datetime_diff('day', ActualDeliveryDate, ExpectedDeliveryDate)
| where DelayDays > 5
| summarize 
    LateDeliveries = count(),
    AvgDelayDays = avg(DelayDays),
    MaxDelayDays = max(DelayDays)
  by SupplierID, bin(OrderDate, 7d)
| where LateDeliveries > 3
| order by AvgDelayDays desc

// inventory_alerts.kql
// Out-of-stock alert query
InventorySnapshot
| where StockOnHand == 0
| join kind=leftouter (
    DimProducts | project ProductID, ProductName, Category
) on ProductID
| join kind=leftouter (
    DimStores | project StoreID, StoreName, Region
) on StoreID
| project Region, StoreName, ProductName, Category, 
          LastRestockDate, DaysOutOfStock = datetime_diff('day', now(), LastRestockDate)
| order by DaysOutOfStock desc
```

---

### 7. Deployment Pipeline Configuration

```
Dev → Test → Prod Promotion Rules:

✅ Pre-deployment checks:
   - Run impact analysis on downstream reports
   - Validate semantic model schema changes
   - Check RLS definitions haven't been modified
   - Confirm sensitivity labels are present on Gold datasets

✅ Automated via deployment pipeline:
   - Lakehouses (Bronze, Silver, Gold)
   - Data pipelines
   - Notebooks
   - Semantic models (via XMLA endpoint)
   - Power BI reports

✅ Version control (Azure DevOps):
   - Semantic models committed as .bim / TMDL
   - Notebooks committed as .ipynb
   - Pipelines committed as .json
   - Branch strategy: feature/* → dev → test → main (prod)
```

---

## 📈 Executive Dashboard KPIs

| KPI | Description | DAX Measure |
|-----|-------------|-------------|
| Total Net Sales | Revenue after discounts | `[Total Net Sales]` |
| Gross Margin % | Profitability rate | `[Gross Margin %]` |
| YoY Sales Growth | Year-over-year comparison | `[Sales YoY Growth %]` |
| Out-of-Stock Rate | Inventory health | `[Out of Stock Rate]` |
| On-Time Delivery % | Supplier performance | `[On Time Delivery Rate]` |
| Sales per Region | Regional breakdown (RLS-filtered) | `[Total Net Sales]` + region slicer |
| Reorder Alerts | Products requiring restocking | `[Reorder Required Count]` |

---

## 🎯 DP-600 Domains Covered

| Domain | Coverage | Implementation |
|--------|----------|---------------|
| **Implement and manage a data analytics solution** | ✅ Implemented | Workspace/capacity design (`RetailCap`, dev/test/prod), Git-backed repo |
| **Prepare and serve data** | ✅ Implemented | Working Bronze/Silver/Gold pipeline (PySpark, runnable) |
| **Implement and manage semantic models** | ✅ Implemented | DAX measure library, Direct Lake-ready star schema |
| **Explore and analyze data** | 🔶 Designed | KQL queries written against a modeled Eventhouse schema (not deployed) |
| **Security & governance** | ✅ Implemented | Security-group access matrix, dynamic RLS, OLS on pricing columns |
| **Lifecycle management** | 🔶 Designed | Dev→test→prod promotion checklist and workspace strategy (pipeline not deployed) |
| **Data quality** | ✅ Implemented | Intentional dedup/null/naming issues built into the data, handled in the Silver transform |

---

## 🚀 Getting Started

### Run it yourself
- **In Fabric:** create a Lakehouse, open a new notebook, attach the Lakehouse, paste in
  [`notebooks/medallion_fabric.py`](notebooks/medallion_fabric.py), and **Run all**. It pulls
  the raw CSVs straight from this repo's GitHub URLs — no upload needed — and writes
  `bronze_*` → `silver_*` → `gold_sales_enriched` / `gold_sales_by_category_region` as Delta tables.
- **Locally (no Fabric access needed):**
  ```bash
  pip install pandas pyarrow matplotlib
  python notebooks/medallion_local.py   # builds ../output/gold_*
  python notebooks/make_charts.py       # builds ../docs/images/*.png
  ```

### Applying the DAX / RLS / KQL artifacts
- Import `06_semantic_model/measures/*.dax` into a Power BI semantic model built on the Gold tables.
- Apply the RLS role and OLS column rules documented in `07_security/rls_definitions.md`.
- Point the `08_kql/*.kql` queries at an Eventhouse fed by a streaming version of the sales/delivery data.

---

## 🔄 Migration Approach: Synapse/Dataflows → Fabric

The medallion pipeline above is written the way I'd structure a **migration** of an existing
Synapse + Power BI dataflow environment into Fabric, not just a greenfield build:

| Legacy asset | Fabric target | Migration note |
|---|---|---|
| Synapse Serverless SQL views / Spark notebooks | Lakehouse notebooks (PySpark) writing Delta | Same transform logic, swap `saveAsTable` for the Lakehouse instead of external tables |
| Power BI dataflows (Power Query / M) doing cleansing | Silver-layer notebook transforms | Moves cleansing off the dataflow refresh clock and into the pipeline, so it's version-controlled and testable |
| Import-mode datasets refreshed nightly | Direct Lake semantic model over Gold tables | Removes the separate dataset refresh step entirely |
| Ad hoc workspace access | Security-group-based workspace roles + RLS/OLS (`07_security/`) | Matches "individual grants → group-based access" pattern common in legacy Power BI environments |
| Manual promotion between environments | Fabric deployment pipelines, dev → test → prod | See `09_deployment/pre_deployment_checks.md` for the promotion checklist |

In practice this is the same sequencing I'd use on a real migration: stand up Bronze/Silver/Gold
in parallel with the legacy dataflows, validate Gold output against the existing Power BI numbers,
then cut reports over to Direct Lake once parity is confirmed — rather than a big-bang cutover.

---

Author: Erick Kiprotich Yegon, epidemiologist and data scientist (real-world evidence, HEOR, causal inference) · Portfolio: https://erickyegon.github.io · LinkedIn: https://linkedin.com/in/erickyegon

---

*Raw source data for this project lives in the repository's [`data/`](data/) folder.*
