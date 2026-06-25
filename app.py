from flask import Flask, jsonify, render_template
from flask_cors import CORS
import asyncio
import json
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

        raw = asyncio.run(
            moviebox_get(
                "/wefeed-h5api-bff/home?host=moviebox.ph"
            )
        )
        text = raw["text"]

        print("RAW RESPONSE:")
        print(text[:5000])

        parsed = json.loads(text)
        anime_list = []

        for section in parsed["data"]["operatingList"]:

            print(section.get("title"))
            print(section.get("type"))

            if (
                section.get("type") ==
            "SUBJECTS_MOVIE":
                and section.get("title") ==
            "Anime[English Dubbed]"
            ):
                for subject in section.get(
                    "subjects",
                    []
                ):

                    anime_list.append({

                        "title": subject.get(
                            "title",
                            "Unknown"
                        ),

                        "image": subject.get(
                            "cover",
                            {}
                        ).get(
                            "url",
                            ""
                        ),

                        "rating": subject.get(
                            "imdbRatingValue",
                            "N/A"
                        ),

                        "year": subject.get(
                            "releaseDate",
                            ""
                        )[:4],

                        "episodes": "Anime",

                        "tags": subject.get(
                            "genre",
                            ""
                        ).split(",")

                    })

        return jsonify(anime_list)
    except Exception as e:

        return jsonify({
            "error": str(e),
            "raw": raw["text"][:3000]
        }), 500
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
