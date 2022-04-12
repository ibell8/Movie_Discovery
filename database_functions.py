from database import DB
import models


def get_comments(identification):
    """This function will query for the relevant comments
    and return them to diaply.
    """
    movie_comments = models.Comment.query.filter_by(movie_id=identification).all()
    return movie_comments


def get_my_comments(current_user):
    """This funtion will be called from app.py, when we go to the route
    "/get_my_comments" and this will return all the comments from a user"""
    movie_comments = models.Comment.query.filter_by(current_user=current_user).all()
    user_rating = []
    user_comment = []
    user_comment_id = []
    movie_id = []
    user = []
    for comm in movie_comments:
        user_rating.append(comm.rating)
        user_comment.append(comm.comment)
        user_comment_id.append(comm.id)
        movie_id.append(comm.movie_id)
        user.append(comm.current_user)
    return user_rating, user_comment, user_comment_id, movie_id, user


def updatedcomments(newcommentsrating):
    """This function will delete or update a comments rating"""
    for newcommrate in newcommentsrating:
        comment_index = newcommrate["comment_id"]
        original = models.Comment.query.filter_by(id=comment_index).first()
        originalrate = original.rating
        if int(newcommrate["rating"]) < 0:
            DB.session.delete(original)
            DB.session.commit()
        elif originalrate != newcommrate["rating"]:
            DB.session.delete(original)
            DB.session.add(
                models.Comment(
                    movie_id=newcommrate["movie_id"],
                    current_user=newcommrate["user"],
                    comment=newcommrate["comment"],
                    rating=int(newcommrate["rating"]),
                )
            )
            DB.session.commit()
