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
├── 📂 01_data/
│   ├── raw/
│   │   ├── pos_data/
│   │   │   └── fact_sales.csv              # 500K rows POS transactions
│   │   └── sap_exports/
│   │       └── fact_supplier_deliveries.csv # 40K rows (with intentional DQ issues)
│   └── dimensions/
│       ├── dim_stores.csv                  # 1,685 stores across NA & Europe
│       ├── dim_products.csv                # 268 products across 6 categories
│       ├── dim_suppliers.csv               # 58 suppliers (8 duplicates embedded)
│       ├── dim_date.csv                    # 1,096 days (2022–2024)
│       └── security_groups.csv             # 18 security group definitions
│
├── 📂 02_bronze/
│   └── notebooks/
│       ├── ingest_pos_sales.ipynb          # POS → Bronze Lakehouse
│       └── ingest_sap_deliveries.ipynb     # SAP CSV → Bronze (with error handling)
│
├── 📂 03_silver/
│   └── notebooks/
│       ├── transform_sales.ipynb           # Enrich: gross margin, net sales calc
│       ├── clean_suppliers.ipynb           # Deduplicate + standardize suppliers
│       ├── transform_deliveries.ipynb      # Null handling, file naming validation
│       └── transform_inventory.ipynb       # Reorder status + DQ checks
│
├── 📂 04_gold/
│   └── notebooks/
│       ├── build_fact_sales_gold.ipynb     # Star schema fact table
│       ├── build_fact_inventory_gold.ipynb
│       ├── build_fact_deliveries_gold.ipynb
│       └── build_dimensions_gold.ipynb     # Conformed dims
│
├── 📂 05_pipelines/
│   ├── pipeline_pos_ingestion.json         # ForEach + Copy Data + error handling
│   ├── pipeline_sap_ingestion.json         # Parameterized + retry logic
│   └── pipeline_master_orchestrator.json   # Master pipeline with dependencies
│
├── 📂 06_semantic_model/
│   ├── CertiAce_Model.bim                  # Semantic model definition (TMSL)
│   ├── measures/
│   │   ├── sales_measures.dax              # Core sales KPIs
│   │   ├── time_intelligence.dax           # MTD, QTD, YTD, YoY
│   │   ├── inventory_measures.dax          # Out-of-stock, reorder rates
│   │   └── supplier_measures.dax           # Delivery performance
│   └── CertiAce_Template.pbit              # Power BI template file
│
├── 📂 07_security/
│   ├── rls_definitions.md                  # Row-level security DAX filters
│   ├── ols_definitions.md                  # Object-level security (supplier pricing)
│   ├── sensitivity_labels.md               # Gold dataset labeling
│   └── workspace_access_matrix.md          # Group → Workspace → Role mapping
│
├── 📂 08_kql/
│   ├── realtime_sales_monitor.kql          # KQL queries for Eventhouse
│   ├── delivery_anomaly_detection.kql      # Late delivery alerting
│   └── inventory_alerts.kql               # Out-of-stock KQL dashboard
│
├── 📂 09_deployment/
│   ├── deployment_pipeline_config.json     # Dev → Test → Prod config
│   ├── pre_deployment_checks.md            # Impact analysis checklist
│   └── rollback_procedure.md
│
├── 📂 10_docs/
│   ├── data_dictionary.md                  # All tables, columns, definitions
│   ├── architecture_decisions.md           # ADRs for key design choices
│   └── business_glossary.md
│
└── README.md
```

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
| **Implement and manage a data analytics solution** | ✅ Full | Workspace setup, capacity management, Git integration |
| **Prepare and serve data** | ✅ Full | Bronze/Silver/Gold pipelines, PySpark, T-SQL |
| **Implement and manage semantic models** | ✅ Full | Direct Lake, incremental refresh, DAX, RLS, OLS |
| **Explore and analyze data** | ✅ Full | KQL queries, Power BI reports, Eventhouse |
| **Security & governance** | ✅ Full | Security groups, RLS, OLS, sensitivity labels, endorsement |
| **Lifecycle management** | ✅ Full | Deployment pipelines, Git, XMLA endpoint, impact analysis |
| **Data quality** | ✅ Full | Duplicate removal, null handling, quarantine pattern |

---

## 🚀 Getting Started

### Prerequisites
- Microsoft Fabric trial or F128 capacity
- Azure DevOps organization (for Git integration)
- Power BI Desktop (for `.pbit` template)

### Setup Steps
1. Clone this repo and connect to Azure DevOps
2. Create four workspaces in Fabric: `ws_retail_dev`, `ws_retail_test`, `ws_retail_prod`, `ws_experiment_sandbox`
3. Upload raw CSVs to Bronze Lakehouse `Files/` section
4. Run notebooks in order: `02_bronze` → `03_silver` → `04_gold`
5. Import semantic model via XMLA endpoint
6. Configure deployment pipeline Dev → Test → Prod
7. Apply security groups and RLS/OLS definitions

---

## 👤 Author

**Erick Kiprotich Yegon, PhD**
Microsoft Certified: Fabric Analytics Engineer Associate (DP-600) · Power BI Data Analyst Associate (PL-300)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/erick-yegon-phd-4116961b4/)
[![GitHub](https://img.shields.io/badge/GitHub-erickyegon-181717?style=flat&logo=github)](https://github.com/erickyegon)

---

*This project is part of the [YegonFabricLabs](https://github.com/erickyegon/DP600) portfolio — demonstrating enterprise-scale Microsoft Fabric implementations.*
