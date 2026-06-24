from flask import Flask, jsonify, render_template
from flask_cors import CORS
import asyncio
from moviebox_client import moviebox_get


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/anime")
def anime_page():
    return render_template("home-anime.html")

@app.route("/mylist")
def mylist():
    return render_template("home-mylist.html")

@app.route("/profile")
def profile():
    return render_template("home-profile.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/api/anime")
def anime():

    try:

        data = asyncio.run(
            moviebox_get(
                "/wefeed-h5api-bff/home?host=moviebox.ph"
            )
        )

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
