import os
import random
import json
import flask
from flask_login import login_user, LoginManager, login_required, current_user
import psycopg2  # There's a pylint error for unused import, but heroku needs this import.
from database import APP
from database import DB, BP
from database_functions import get_comments, get_my_comments, updatedcomments
import models
from movieapi import gather_data
from wikiapi import get_urls

MOVIE_ID = ["155", "5175", "5174"]
MOVIE_NAMES, MOVIE_GENRES, MOVIE_TAGLINES, MOVIE_IMAGES = gather_data(MOVIE_ID)
MOVIE_LINKS = get_urls(MOVIE_NAMES)
MOVIE_LASTGENRE = []
for g in MOVIE_GENRES:
    MOVIE_LASTGENRE.append(g.pop())

LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
LOGIN_MANAGER.login_view = "login"


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    # This will get the object for our login
    return models.User.query.get(user_id)


@APP.route("/get_my_comments")
def getcomments():
    (
        user_rating,
        user_comment,
        user_comment_id,
        user_movie_id,
        currentuser,
    ) = get_my_comments(current_user.username)
    build_comment = []
    for i in range(
        0, len(user_comment)
    ):  # I'm using a range rather than an enumerate because it's the better option
        build_comment.append(
            {
                "comment_id": user_comment_id[i],
                "comment": user_comment[i],
                "rating": user_rating[i],
                "user": currentuser[i],
                "movie_id": user_movie_id[i],
            }
        )
    return flask.jsonify(build_comment)


@APP.route("/update_my_comments", methods=["GET", "POST"])
def update_comments():
    print("Got to here")
    newcomments_and_ratings = flask.request.json
    updatedcomments(newcomments_and_ratings)
    return flask.redirect("/movie")


# route for serving React page
@APP.route("/comments")
def index():
    # NB: DO NOT add an "index.html" file in your normal templates folder
    # Flask will stop serving this React page correctly
    return flask.render_template("index.html")


@APP.route("/movie")
@login_required
def movie():
    """Shows movies with the comment section
    When logged in
    """
    APP.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    random_num = random.randint(0, 2)
    movie_comments = get_comments(MOVIE_ID[random_num])
    return flask.render_template(
        "movie.html",
        name=MOVIE_NAMES[random_num],
        genres=MOVIE_GENRES[random_num],
        tagline=MOVIE_TAGLINES[random_num],
        image=MOVIE_IMAGES[random_num],
        link=MOVIE_LINKS[random_num],
        last=MOVIE_LASTGENRE[random_num],
        random_num=random_num,
        movie_id=MOVIE_ID[random_num],
        movie_comments=movie_comments,
    )


@APP.route("/", methods=["GET", "POST"])
def login():
    """This is the screen when we first load the app,
    and it will handle our login process.
    """
    APP.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    if flask.request.method == "GET":
        return flask.render_template("login.html")
    data = flask.request.form
    username = data["username"]
    user = models.User.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect("/movie")
    flask.flash("Username doesn't exist, register new username")
    return flask.render_template("login.html")


@APP.route("/register", methods=["GET", "POST"])
def register():
    """The route we take for registration
    This will handle our username and
    get us in the system.
    """
    if flask.request.method == "POST":
        data = flask.request.form
        username = data["username"]
        if models.User.query.filter_by(username=username).first() is not None:
            flask.flash("Username was already in use")
            return flask.redirect("/")
        DB.session.add(models.User(username=username))
        DB.session.commit()
        return flask.redirect("/")
    return flask.render_template("register.html")


@APP.route("/added_comment", methods=["POST"])
def added_comment():
    """We'll use this function to post our
    comments into the database
    """
    movie_data = flask.request.form
    movie_identification = movie_data["Movie_ID"]
    movie_comment = movie_data["comment"]
    movie_rating = movie_data["rating"]
    if movie_comment == "" or movie_rating == "" or len(movie_comment) > 200:
        flask.flash("For review to be added, you need both a comment and rating")
        return flask.redirect("/movie")
    DB.session.add(
        models.Comment(
            movie_id=movie_identification,
            current_user=current_user.username,
            comment=movie_comment,
            rating=int(movie_rating),
        )
    )
    DB.session.commit()
    return flask.redirect("/movie")


if __name__ == "__main__":
    APP.secret_key = os.getenv("SECRET_KEY")
    APP.run(
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
