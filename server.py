"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, connect_to_db, db


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


@app.route('/register', methods=["GET"])
def register_form():

    return render_template("user_login.html")


@app.route('/register', methods=["POST"])
def register_process():

    username = request.form.get("username")

    password = request.form.get("password")


    entered_email = db.session.query(User).filter_by(email=username).all()

    entered_password = db.session.query(User).filter_by(password=password).all()

    # Pick up here on Wednesday

    if username in entered_email and password in entered_password:
        return redirect("/")
    else:
        flash("Login details incorrect")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
