from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

edit_profile = Blueprint("edit_profile", __name__)

@edit_profile.route("/edit_profile", methods=["GET", "POST"])
def edit_profile_page():
    if request.method == "POST":
        connection = sqlite3.connect("arbor_db.db")
        cursor = connection.cursor()

        cursor.execute("SELECT name, description, email_1, email_2, mobile_no_1, mobile_no_2, facebook, instagram, twitter, linkedin, youtube, github, tiktok, pinterest FROM profile WHERE user_id = ?", (session["user_id"],))
        existing = cursor.fetchone()

        if existing:
            name = request.form.get("name", "").strip() or existing[0]
            description = request.form.get("description", "").strip() or existing[1]
            email_1 = request.form.get("email_1", "").strip() or existing[2]
            email_2 = request.form.get("email_2", "").strip() or existing[3]
            mobile_no_1 = request.form.get("mobile_no_1", "").strip() or existing[4]
            mobile_no_2 = request.form.get("mobile_no_2", "").strip() or existing[5]
            facebook = request.form.get("facebook", "").strip() or existing[6]
            instagram = request.form.get("instagram", "").strip() or existing[7]
            twitter = request.form.get("twitter", "").strip() or existing[8]
            linkedin = request.form.get("linkedin", "").strip() or existing[9]
            youtube = request.form.get("youtube", "").strip() or existing[10]
            github = request.form.get("github", "").strip() or existing[11]
            tiktok = request.form.get("tiktok", "").strip() or existing[12]
            pinterest = request.form.get("pinterest", "").strip() or existing[13]

            cursor.execute("""
                UPDATE profile
                SET name=?, description=?, email_1=?, email_2=?, mobile_no_1=?, mobile_no_2=?, facebook=?, instagram=?, twitter=?, linkedin=?, youtube=?, github=?, tiktok=?, pinterest=?
                WHERE user_id=?
            """, (name, description, email_1, email_2, mobile_no_1, mobile_no_2, facebook, instagram, twitter, linkedin, youtube, github, tiktok, pinterest, session["user_id"]))
        else:
            # Insert new profile if none exists
            cursor.execute("""
                INSERT INTO profile(name, description, email_1, email_2, mobile_no_1, mobile_no_2, facebook, instagram, twitter, linkedin, youtube, github, tiktok, pinterest, user_id)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, description, email_1, email_2, mobile_no_1, mobile_no_2, facebook, instagram, twitter, linkedin, youtube, github, tiktok, pinterest, session["user_id"]))

        connection.commit()
        connection.close()
        flash("Profile Updated Successfully ✅")
        return redirect(url_for("dashboard.dashboard_page"))

    return render_template("dashboard/edit_profile.html")