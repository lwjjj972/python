# 数据库配置常量
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "db_douban",
    "charset": "utf8mb4"
}

import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(os.path.dirname(BASE_PATH), "数据文件夹")
os.makedirs(DATA_PATH, exist_ok=True) 