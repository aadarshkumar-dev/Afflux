from flask import Blueprint, render_template, session, flash, redirect, url_for
import sqlite3

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
def dashboard_page():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("auth.login"))
    
    connection = sqlite3.connect("arbor_db.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
    SELECT profile.name, profile.description, users.username
    FROM profile
    JOIN users ON profile.user_id = users.id
    WHERE users.id = ?
    """, (session["user_id"],))
    profile = cursor.fetchone()
    connection.close()

    return render_template("dashboard/dashboard.html", profile=profile)

@dashboard.route("/contacts")
def contacts_page():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("auth.login"))
    
    with sqlite3.connect("arbor_db.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM profile WHERE user_id = ?", (session["user_id"],))
        values = cursor.fetchone()
    return render_template("dashboard/contacts.html", values=values)