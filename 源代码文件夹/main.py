import requests
import re
import time
import pymysql
import os
import pandas as pd

# ---------- 数据库配置 ----------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'db_douban',
    'charset': 'utf8mb4'
}

DATA_DIR = "../数据文件夹"
os.makedirs(DATA_DIR, exist_ok=True)
movie_all = []  # 用来存所有电影，导出Excel
# ===========================================================

def get_conn():
    return pymysql.connect(**DB_CONFIG)

def save_to_db(movie):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
    INSERT INTO movie
    (movie_id, title, rating, year, tags, intro, cover_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        title=VALUES(title),
        rating=VALUES(rating),
        year=VALUES(year),
        tags=VALUES(tags),
        intro=VALUES(intro),
        cover_url=VALUES(cover_url)
    """
    cur.execute(sql, (
        movie['movie_id'],
        movie['title'],
        movie['rating'],
        movie['year'],
        movie['tags'],
        movie['intro'],
        movie['cover_url']
    ))
    conn.commit()
    cur.close()
    conn.close()

# ---------- 爬虫主体 ----------
def crawl_douban():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    for page in range(0, 250, 25):
        url = f"https://movie.douban.com/top250?start={page}"
        print(f"\n正在爬取：第 {page//25 + 1} 页")

        try:
            time.sleep(1.2)
            resp = requests.get(url, headers=headers, timeout=15)

            if resp.status_code != 200:
                print("请求被拦截，跳过当前页")
                continue

            html = resp.text

            items = re.findall(r'<div class="item">.*?</div>\s*</div>\s*</div>', html, re.S)
            if not items:
                print("未提取到数据，可能被反爬")
                continue

            for item in items:
                # 1. 排名
                rank = re.search(r'<em.*?>(\d+)</em>', item, re.S)
                rank = rank.group(1) if rank else "0"

                # 2. 片名
                title = re.search(r'<span class="title">([^<&]+?)</span>', item)
                title = title.group(1) if title else "无片名"

                # 3. 评分
                score = re.search(r'<span class="rating_num" property="v:average">(\d+\.\d+)</span>', item)
                score = score.group(1) if score else "0.0"

                # 4. 评价人数
                people = re.search(r'(\d+)人评价', item)
                people = people.group(1) if people else "0"

                # 5. 评语
                quote = re.search(r'<p class="quote">\s*<span>(.*?)</span>\s*</p>', item, re.S)
                quote = quote.group(1) if quote else "无评语"

                # 6. 年份 + 类型
                p_tag = re.search(r'<p>\s*(.*?)\s*</p>', item, re.S)
                p_text = p_tag.group(1) if p_tag else ""

                year = re.search(r'(\d{4})', p_text)
                year = year.group(1) if year else "未知"

                tags = ""
                parts = p_text.split("/")
                if len(parts) >= 3:
                    tags = parts[-1].strip()
                    tags = tags.replace("&nbsp;", "").strip()

                # 封面置空
                cover_url = ""

                movie_id = f"top250_{rank}"

                movie = {
                    "movie_id": movie_id,
                    "title": title,
                    "rating": float(score),
                    "year": year,
                    "tags": tags,
                    "intro": quote,
                    "cover_url": cover_url
                }

                print(f"排名：{rank} | 片名：{title} | 评分：{score} | 年份：{year} | 类型：{tags} | 评价人数：{people} | 评语：{quote} |")
                
                movie_all.append(movie)
                save_to_db(movie)

        except Exception as e:
            print(f"出错：{e}")

    df = pd.DataFrame(movie_all)
    df.to_excel(f"{DATA_DIR}/top250电影_原始数据.xlsx", index=False, engine="openpyxl")
    print(f"\n✅ Excel 已保存到：{DATA_DIR}/top250电影.xlsx")

if __name__ == "__main__":
    print("开始爬取豆瓣Top250（最终稳定版）...")
    crawl_douban()
    print("\n爬取结束！")