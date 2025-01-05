import os
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helper import apology , login_required 




app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/')
# @login_required
def home():
    schemes = [
        {
            "name": "Pradhan Mantri Jan Dhan Yojana",
            "link": "https://pmjdy.gov.in/",
            "tags": ["financial", "inclusion"]
        },
        {
            "name": "Ayushman Bharat",
            "link": "https://www.pmjay.gov.in/",
            "tags": ["medical", "healthcare"]
        },
        {
            "name": "Pradhan Mantri Awas Yojana",
            "link": "https://pmaymis.gov.in/",
            "tags": ["housing", "urban development"]
        },
        {
            "name": "National Scholarship Portal",
            "link": "https://scholarships.gov.in/",
            "tags": ["education", "scholarship"]
        },
        {
            "name": "Atal Pension Yojana",
            "link": "https://npscra.nsdl.co.in/scheme-details/APY.php",
            "tags": ["financial", "pension"]
        }
    ]
    return render_template('index.html',schemes=schemes)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted21``
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    


if __name__ == '__main__':
    app.run(debug=True)