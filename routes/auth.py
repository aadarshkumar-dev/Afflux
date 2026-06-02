from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
import re
import bcrypt

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        normalized_username = username.lower()

        # ---------------- VALIDATION FIRST ----------------
        if not username or not password:
            flash("Please fill in both username and password.")
            return redirect(url_for("auth.signup"))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.")
            return redirect(url_for("auth.signup"))

        if not re.match(r'^[A-Za-z0-9_.]+$', username):
            flash("Username must contain only letters, numbers, \"_\" , or \".\"")
            return redirect(url_for("auth.signup"))

        # ---------------- DATABASE CHECK ----------------
        connection = sqlite3.connect("arbor_db.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT username FROM users WHERE username = ?",
            (normalized_username,)
        )
        existing = cursor.fetchone()

        if existing:
            connection.close()
            flash("This username is already taken. Please choose another one.")
            return redirect(url_for("auth.signup"))

        # ---------------- HASH PASSWORD ----------------
        hashed_password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )
        hashed_password = hashed_password.decode("utf-8")

        # ---------------- INSERT USER ----------------
        connection = sqlite3.connect("arbor_db.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users(username, password) VALUES(?, ?)",
            (normalized_username, hashed_password)
        )
        user_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO profile(name, user_id) VALUES(?, ?)",
            (normalized_username[:40], user_id)
        )

        connection.commit()
        connection.close()

        session["user_id"] = user_id
        session["username"] = normalized_username

        flash(f"Welcome to Afflux, {normalized_username}! 🎉 Your account has been created.")
        return redirect(url_for("dashboard.dashboard_page"))

    return render_template("auth/signup.html")

# ---------------------------------------------------------- login --------------------------------------------------------

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username").strip().lower()
        password = request.form.get("password")

        if not username or not password:
            flash("Please fill in both username and password.")
            return redirect(url_for("auth.login"))
        
        connection = sqlite3.connect("arbor_db.db")
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user[2].encode()):
            connection.close()
            session["user_id"] = user[0]
            session["username"] = user[1]
            flash(f"Login Successful {session['username']}")
            return redirect(url_for("dashboard.dashboard_page"))
        else:
            connection.close()
            flash("Invalid credentials")
            return redirect(url_for("auth.login"))            

    return render_template("auth/login.html")