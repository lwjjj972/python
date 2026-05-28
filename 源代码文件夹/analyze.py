import pandas as pd
import numpy as np
import os

# ====================== 路径配置 ======================
DATA_DIR = "../数据文件夹"
input_file = os.path.join(DATA_DIR, "top250电影_原始数据.xlsx")
output_file = os.path.join(DATA_DIR, "top250电影_数据.xlsx")
report_file = os.path.join(DATA_DIR, "数据分析报告.txt")

# ====================== 1. 数据加载 ======================
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        print(f"✅ 原始数据读取成功，共 {len(df)} 条")
        print("原始字段：", list(df.columns))
        return df
    except FileNotFoundError:
        print(f"❌ 错误：未找到文件 {file_path}")
        return None

# ====================== 2. 数据清洗 ======================
def clean_data(df):
    print("\n===== 数据清洗开始 =====")

    # 1. 查看缺失值
    print("缺失值情况：")
    print(df.isnull().sum())

    # 2. 核心字段缺失处理（删除）
    df = df.dropna(subset=["title", "rating", "year"])

    # 3. 数据类型转换
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["rating"])

    # 4. 去重（按电影名去重）
    df = df.drop_duplicates(subset=["title"], keep="first")

    # 5. 异常值过滤
    df = df[(df["rating"] >= 0) & (df["rating"] <= 10)]

    print(f"✅ 清洗完成，有效数据：{len(df)} 条")
    return df

# ====================== 3. 统计分析 ======================
def analyze_data(df):
    # 评分统计
    rating_mean = np.mean(df["rating"])
    rating_median = np.median(df["rating"])
    rating_std = np.std(df["rating"], ddof=1)

    # 按年份统计（黄金年份）
    year_count = df.groupby("year")["title"].count().reset_index()
    year_count.columns = ["year", "movie_num"]
    golden_year = year_count.loc[year_count["movie_num"].idxmax()]

    # 评分最高TOP10
    top10_rating = df.sort_values("rating", ascending=False).head(10)[
        ["movie_id", "title", "year", "rating", "tags"]
    ]

    return {
        "rating_stats": {
            "均值": round(rating_mean, 2),
            "中位数": round(rating_median, 2),
            "标准差": round(rating_std, 2)
        },
        "golden_year": {
            "年份": int(golden_year["year"]),
            "上榜数量": golden_year["movie_num"]
        },
        "top10_rating": top10_rating
    }

# ====================== 4. 生成报告 ======================
def generate_report(result, df_clean):
    report = f"""
====================== 豆瓣TOP250电影数据分析报告 ======================
✅ 数据清洗完成
✅ 有效电影数量：{len(df_clean)} 部

📊 评分统计
   平均分：{result['rating_stats']['均值']}
   中位数：{result['rating_stats']['中位数']}
   标准差：{result['rating_stats']['标准差']}

🏆 黄金年份（上榜电影最多）
   {result['golden_year']['年份']} 年（上榜 {result['golden_year']['上榜数量']} 部）

🔥 评分最高 TOP10 电影
{result['top10_rating'].to_string(index=False)}
=====================================================================
"""
    print(report)

    # 写入txt报告
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✅ 分析报告已保存到：{report_file}")

    # 写入清洗后的Excel
    df_clean.to_excel(output_file, index=False)
    print(f"✅ 清洗后数据已保存到：{output_file}")

# ====================== 主程序 ======================
if __name__ == "__main__":
    df_raw = load_data(input_file)
    if df_raw is not None:
        df_clean = clean_data(df_raw)
        result = analyze_data(df_clean)
        generate_report(result, df_clean)