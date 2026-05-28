import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

DATA_DIR = "../数据文件夹"
excel_path = f"{DATA_DIR}/top250电影_数据.xlsx"

df = pd.read_excel(excel_path)
df = df.dropna(subset=["year"])
df["year"] = pd.to_numeric(df["year"], errors="coerce")

# ---------------- 图1：评分分布 ----------------
plt.figure(figsize=(10,5))
plt.hist(df["rating"], bins=12, color="skyblue", edgecolor="black")
plt.title("豆瓣TOP250电影评分分布")
plt.xlabel("评分")
plt.ylabel("数量")
plt.savefig(f"{DATA_DIR}/图1_评分分布直方图.png", bbox_inches="tight")
plt.close()

# ---------------- 图2：年份折线图 ----------------
year_count = df["year"].value_counts().sort_index()
plt.figure(figsize=(12,5))
plt.plot(year_count.index, year_count.values, marker="o", color="red")
plt.title("各年份上榜电影数量")
plt.xlabel("年份")
plt.ylabel("电影数")
plt.savefig(f"{DATA_DIR}/图2_年份数量折线图.png", bbox_inches="tight")
plt.close()

# ---------------- 图3：评分TOP10柱状图 ----------------
top10 = df.sort_values("rating", ascending=False).head(10)
plt.figure(figsize=(12,5))
plt.bar(top10["title"], top10["rating"], color="orange")
plt.xticks(rotation=30, ha="right")
plt.title("豆瓣TOP250评分TOP10")
plt.ylabel("评分")
plt.ylim(8.5, 10)
plt.savefig(f"{DATA_DIR}/图3_Top10柱状图.png", bbox_inches="tight")
plt.close()

print("✅ 3张图片已保存到：数据文件夹/")