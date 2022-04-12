import json
from flask_login import UserMixin
from database import DB


class User(DB.Model, UserMixin):
    """This will create the user object
    portion of our database and hold the users.
    """

    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(20), unique=True, nullable=False)

    def __repr__(self):
        return "<Person %r>" % self.username


class Comment(DB.Model):
    """This will create out comment object portion,
    which will be stored in our database.
    """

    id = DB.Column(DB.Integer, primary_key=True)
    movie_id = DB.Column(DB.String(200), nullable=False)
    comment = DB.Column(DB.String(200), nullable=False)
    rating = DB.Column(DB.Integer, nullable=False)
    current_user = DB.Column(DB.String(200), nullable=False)

    def __repr__(self):
        return "User: %s commented: %s.\nThen gave the movie" " a score of: %d." % (
            self.current_user,
            self.comment,
            self.rating,
        )
