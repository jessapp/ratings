"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1,3])


    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/movies')
def movie_list():
    """Show list of movies"""

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movie_list.html", movies=movies)

@app.route('/login', methods=["GET"])
def register_form():

    return render_template("user_login.html")


@app.route('/login', methods=["POST"])
def register_process():

    username = request.form.get("username")

    password = request.form.get("password")

    try:
        db.session.query(User).filter_by(email=username).one().email
        password == db.session.query(User).filter_by(email=username).one().password
    except NoResultFound:
        flash("Login information inccorect")
        return redirect("/login")

    user_id = db.session.query(User).filter_by(email=username).one().user_id

    session['username'] = username
    flash("Logged in!")


    return redirect("/users/" + str(user_id))


@app.route('/logout', methods=["GET"])
def logout():

    return render_template("logout_form.html")


@app.route('/logout', methods=["POST"])
def logout_complete():

    del session["username"]
    flash("Logged out!")

    return redirect("/")


@app.route('/register', methods=["GET"])
def register():

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_complete():

    email = request.form.get("email")

    password = request.form.get("password")

    age = request.form.get("age")

    zipcode = request.form.get("zipcode")

    new_user = User(email=email,
                    password=password,
                    age=age,
                    zipcode=zipcode)


    db.session.add(new_user)

    db.session.commit()

    session['username'] = email
    flash("Logged in!")

    return redirect("/")

@app.route('/users/<user_id>')
def display_user(user_id):


    age = db.session.query(User).filter_by(user_id=user_id).one().age  
    
    zipcode = db.session.query(User).filter_by(user_id=user_id).one().zipcode

    movies = db.session.query(Rating).filter_by(user_id=user_id).all()

    movie_titles = []


    for movie in movies:
        r_movie_id = movie.movie_id
        score = movie.score
        movie_name = db.session.query(Movie).filter_by(movie_id=r_movie_id).one().title
        movie_titles.append((movie_name, score))


    return render_template("user_details.html",
                    age=age,
                    zipcode=zipcode,
                    movie_titles=movie_titles)


@app.route('/movies/<movie_id>', methods=["GET"])
def display_movie(movie_id):


    title = db.session.query(Movie).filter_by(movie_id=movie_id).one().title 
    
    released_at = db.session.query(Movie).filter_by(movie_id=movie_id).one().released_at

    imdb_url = db.session.query(Movie).filter_by(movie_id=movie_id).one().imdb_url

    m_ratings = db.session.query(Rating).filter_by(movie_id=movie_id).all()

    movie_ratings = []


    for rating in m_ratings:
        score = rating.score
        user_id = rating.user_id
        movie_ratings.append((score, user_id))


    return render_template("movie_details.html",
                    title=title,
                    released_at=released_at,
                    imdb_url=imdb_url,
                    movie_ratings=movie_ratings,
                    movie_id=movie_id)


@app.route('/movies/<int:movie_id>', methods=['POST'])
def process_rating(movie_id):

    rating = request.form.get("rating")

    current_email = session['username']
    user_id = db.session.query(User).filter_by(email=current_email).one().user_id


    try:
       new_score = db.session.query(Rating).filter_by(user_id=user_id, movie_id=movie_id).one()
    except NoResultFound:

        new_rating = Rating(user_id=user_id,
                            movie_id=movie_id,
                            score=rating)

        db.session.add(new_rating)

        db.session.commit()

        return redirect("/movies/" + str(movie_id))

    new_score.score = rating

    db.session.commit()

    return redirect("/movies/" + str(movie_id))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
