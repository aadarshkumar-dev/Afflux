from flask import Flask, render_template
import os
import sqlite3
from routes.auth import auth
from routes.dashboard import dashboard
from routes.edit_profile import edit_profile


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(edit_profile)

# ------------------------------------------------------- Create Table Users --------------------------------------------------------------

connection = sqlite3.connect("arbor_db.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

connection.commit()
connection.close()

# ------------------------------------------------------- Create Table Profile --------------------------------------------------------------

connection = sqlite3.connect("arbor_db.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS profile(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    email_1 TEXT,
    email_2 TEXT,
    mobile_no_1 TEXT,
    mobile_no_2 TEXT,
    facebook TEXT,
    instagram TEXT,
    twitter TEXT,
    linkedin TEXT,
    youtube TEXT,
    github TEXT,
    tiktok TEXT,
    pinterest TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

connection.commit()
connection.close()

# ------------------------------------------------------- show users --------------------------------------------------------------

@app.route("/show_users")
def show_users():
    connection = sqlite3.connect("arbor_db.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    connection.close()

    return render_template("auth/show_users.html", rows=rows)

# ------------------------------------------------------- show profiles --------------------------------------------------------------

@app.route("/show_profiles")
def show_profiles():
    connection = sqlite3.connect("arbor_db.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM profile")
    hors = cursor.fetchall()
    
    connection.close()
    return render_template("dashboard/show_profiles.html", hors=hors)


@app.route("/")
def home():
    return render_template("main/index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)