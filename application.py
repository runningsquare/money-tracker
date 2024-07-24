from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import usd, login_required, check_input

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///MoneyTracker.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Let user input expenses and income"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure day, month, year was submitted
        day = request.form.get("day")
        month = request.form.get("month")
        year = request.form.get("year")

        if not day:
            return render_template("apology2.html", message="Missing 'day'.")
        if not month:
            return render_template("apology2.html", message="Missing 'month'.")
        if not year:
            return render_template("apology2.html", message="Missing 'year'.")

        # Ensure day is between 1 and 31 and is a positive integer
        if day.isdigit() == False or int(day) < 1 or int(day) > 31:
            return render_template("apology2.html", message="Invalid 'day'.")

        # Ensure month is between 1 and 12 and is a positive integer
        if month.isdigit() == False or int(month) < 1 or int(month) > 12:
            return render_template("apology2.html", message="Invalid 'month'.")

        # Ensure year is between 2000 and 2121 and is a positive integer
        if year.isdigit() == False or int(year) < 2000 or int(year) > 2121:
            return render_template("apology2.html", message="Invalid 'year'.")

        # Ensure expenses and salary inputs are postitive integers or floats
        expenses_food = request.form.get("expenses_food")
        expenses_bills = request.form.get("expenses_bills")
        expenses_transport = request.form.get("expenses_transport")
        expenses_shopping = request.form.get("expenses_shopping")
        expenses_social = request.form.get("expenses_social")
        expenses_education = request.form.get("expenses_education")
        expenses_grocery = request.form.get("expenses_grocery")
        expenses_others = request.form.get("expenses_others")
        expenses_salary = request.form.get("expenses_salary")
        expenses_investment = request.form.get("expenses_investment")

        if check_input(expenses_food) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")
        if check_input(expenses_bills) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")
        if check_input(expenses_transport) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")
        if check_input(expenses_shopping) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")
        if check_input(expenses_social) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")
        if check_input(expenses_education) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")
        if check_input(expenses_grocery) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")
        if check_input(expenses_others) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")
        if check_input(expenses_salary) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")
        if check_input(expenses_investment) == False:
            return render_template("apology2.html", message="Expenses and Income inputs must be a positive integer or float.")

        # Check if input of the same date exists
        rows = db.execute("SELECT * FROM dailyLog WHERE userID = ? AND day = ? AND month = ? AND year = ?",
                          session["user_id"], day, month, year)

        if len(rows) == 1:
            total_food = rows[0]["food"] + float(expenses_food)
            total_bills = rows[0]["bills"] + float(expenses_bills)
            total_transport = rows[0]["transport"] + float(expenses_transport)
            total_shopping = rows[0]["shopping"] + float(expenses_shopping)
            total_social = rows[0]["social"] + float(expenses_social)
            total_education = rows[0]["education"] + float(expenses_education)
            total_grocery = rows[0]["grocery"] + float(expenses_grocery)
            total_others = rows[0]["others"] + float(expenses_others)
            total_salary = rows[0]["salary"] + float(expenses_salary)
            total_investment = rows[0]["investment"] + float(expenses_investment)

            db.execute("UPDATE dailyLog SET food = ?, bills = ?, transport = ?, shopping = ?, social = ?, education = ?, grocery = ?, others = ?, salary = ?, investment = ? WHERE userID = ? AND day = ? AND month = ? AND year =?",
                       total_food, total_bills, total_transport, total_shopping, total_social,
                       total_education, total_grocery, total_others, total_salary,
                       total_investment, session["user_id"], day, month, year)

        # Insert user inputs into dailyLog table
        else:
            db.execute("INSERT INTO dailyLog (userID, day, month, year, food, bills, transport, shopping, social, education, grocery, others, salary, investment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       session["user_id"], day, month, year, expenses_food, expenses_bills,
                       expenses_transport, expenses_shopping, expenses_social,
                       expenses_education, expenses_grocery, expenses_others, expenses_salary,
                       expenses_investment)

        # Update user funds
        rows = db.execute("SELECT funds FROM users WHERE id = ?", session["user_id"])
        user_funds = rows[0]["funds"] - float(expenses_food) - float(expenses_bills) - float(expenses_transport) - float(expenses_shopping) - float(expenses_social) - float(expenses_education) - float(expenses_grocery) - float(expenses_others) + float(expenses_salary) + float(expenses_investment)
        db.execute("UPDATE users SET funds = ? WHERE id = ?", user_funds, session["user_id"])

        # Return to index page
        return render_template("index.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", message="Must provide username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", message="Must provide password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("apology.html", message="Invalid username and/or password.")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", message="Must provide username.")

        # Query username from database
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not exist yet
        if len(rows) != 0:
            return render_template("apology.html", message="Username is not available.")

        # Ensure password was submitted
        if not request.form.get("password"):
            return render_template("apology.html", message="Must provide password.")

        # Ensure password and password confirmation matches
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return render_template("apology.html", message="Passwords don't match.")

        # Hash user's password
        password_hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=len(password))

        # Insert new user into users table
        username = request.form.get("username")
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)

        return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Display user expenses and income history"""
    # Select user history from dailyLog database
    user_history = db.execute("SELECT * FROM dailyLog WHERE userID = ? ORDER BY year DESC, month DESC, day DESC", session["user_id"])

    # Select funds from user
    rows = db.execute("SELECT funds FROM users WHERE id = ?", session["user_id"])
    user_funds = rows[0]["funds"]

    # Go to history page
    return render_template("history.html", user_history=user_history, user_funds=user_funds)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return render_template("apology.html", message="InternalServerError.")

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)