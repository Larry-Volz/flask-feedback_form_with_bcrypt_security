"""Example flask app that stores passwords hashed with Bcrypt. Yay!"""

'''
TODO:
- FIX password in models/forms to be password field instead of text

'''
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm 

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_form"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all() 

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Show homepage with links to site areas."""
    #instructions skipped this step and without it can't go to login

    return render_template("index.html")    


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""
    form = RegisterForm()

    if form.validate_on_submit(): 
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.add(user)
        db.session.commit()

        session['username'] = user.username

        # on successful login, redirect to secret page
        # return redirect(f"/users/{user.username}")
        return redirect(f"/users/{user.username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)
# end-login    


@app.route("/users/<username>")
def secret(username):
    """Example hidden page for logged-in users only."""

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:
        user = User.query.filter_by(username=username).first()  
        return render_template("secret.html", user=user)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("username")
    flash("You have been logged out")

    return redirect("/")
