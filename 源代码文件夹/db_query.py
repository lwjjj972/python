import pymysql
from DbConfig import DB_CONFIG

class DbQuery:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """创建数据库连接"""
        try:
            self.conn = pymysql.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        except pymysql.MySQLError as e:
            print(f"数据库连接失败: {e}")
            raise

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def insert_movie(self, movie_data):
        """插入单条电影数据"""
        sql = """
        INSERT INTO movie (movie_id, title, rating, year, intro, tags, cover_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        title=VALUES(title), rating=VALUES(rating), year=VALUES(year), 
        intro=VALUES(intro), tags=VALUES(tags), cover_url=VALUES(cover_url)
        """
        try:
            self.cursor.execute(sql, (
                movie_data.get('movie_id'),
                movie_data.get('title'),
                movie_data.get('rating'),
                movie_data.get('year'),
                movie_data.get('intro'),
                ','.join(movie_data.get('tags', [])),
                movie_data.get('cover_url')
            ))
            self.conn.commit()
            return True
        except pymysql.MySQLError as e:
            self.conn.rollback()
            print(f"插入电影数据失败: {e}")
            return False

    def get_all_movies(self):
        """查询所有电影数据"""
        sql = "SELECT * FROM movie ORDER BY rating DESC"
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"查询电影数据失败: {e}")
            return []

    def verify_user(self, username, password):
        """验证用户登录"""
        sql = "SELECT * FROM user WHERE username=%s AND password=%s"
        try:
            self.cursor.execute(sql, (username, password))
            return self.cursor.fetchone()
        except pymysql.MySQLError as e:
            print(f"验证用户失败: {e}")
            return None

if __name__ == "__main__":
    db = DbQuery()
    print("数据库连接成功")
    db.close()