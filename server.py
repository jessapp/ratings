"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, connect_to_db, db

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
    """Show lsit of users"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


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

    session['username'] = username
    flash("Logged in!")


    return redirect("/")


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

    movies = db.session.query(Rating).filter_by(user_id=user_id).all().movie_id

    movie_titles = []

    # Start here on Thursday

    for movie_id in movies:
        movie_name = db.session.query(Movie).filter_by(movie_id=movie_id).all().title
        movie_titles.append(movie_name)

    return render_template("user_details.html",
                    age=age,
                    zipcode=zipcode,
                    movie_titles=movie_titles)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
