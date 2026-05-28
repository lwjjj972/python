from flask import Flask, render_template
from db_query import DbQuery
import os

app = Flask(__name__)
app.secret_key = "douban_view_2024"
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = DbQuery()

@app.route("/")
def index():
    movies = db.get_all_movies()
    return render_template("index.html", movies=movies)

@app.route("/movie/list")
def movie_list():
    movies = db.get_all_movies()
    return render_template("list.html", movies=movies)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)