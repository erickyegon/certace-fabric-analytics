"""
Generate portfolio chart images from the Gold layer.
Run medallion_local.py first, then: python notebooks/make_charts.py
Outputs PNGs to ./docs/images.
"""

from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
IMG = ROOT / "docs" / "images"
IMG.mkdir(parents=True, exist_ok=True)

gold = pd.read_parquet(OUT / "gold_sales_enriched.parquet")
TEAL = "#0f8b8d"

def savefig(fig, name):
    fig.tight_layout()
    fig.savefig(IMG / name, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("wrote", IMG / name)

# 1. Net sales by product category
cat = gold.groupby("Category")["NetSales"].sum().sort_values(ascending=True) / 1e6
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(cat.index, cat.values, color=TEAL)
ax.set_xlabel("Net Sales ($M)")
ax.set_title("CertiAce — Net Sales by Product Category")
for i, v in enumerate(cat.values):
    ax.text(v, i, f" {v:,.1f}", va="center", fontsize=9)
savefig(fig, "net_sales_by_category.png")

# 2. Net sales by region
reg = gold.groupby("Region")["NetSales"].sum().sort_values(ascending=True) / 1e6
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(reg.index, reg.values, color="#e07a3f")
ax.set_xlabel("Net Sales ($M)")
ax.set_title("CertiAce — Net Sales by Region")
for i, v in enumerate(reg.values):
    ax.text(v, i, f" {v:,.1f}", va="center", fontsize=9)
savefig(fig, "net_sales_by_region.png")

# 3. Monthly net sales trend
m = (gold.groupby(["Year", "Month"])["NetSales"].sum() / 1e6).reset_index()
m["period"] = m["Year"].astype(str) + "-" + m["Month"].astype(str).str.zfill(2)
m = m.sort_values(["Year", "Month"])
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(m["period"], m["NetSales"], color=TEAL, marker="o", markersize=3, linewidth=1.5)
ax.set_ylabel("Net Sales ($M)")
ax.set_title("CertiAce — Monthly Net Sales Trend")
ax.set_xticks(m["period"][::3])
ax.tick_params(axis="x", rotation=45, labelsize=8)
ax.grid(True, alpha=0.3)
savefig(fig, "monthly_net_sales_trend.png")

print("Charts done.")
