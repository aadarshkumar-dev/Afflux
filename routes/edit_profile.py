from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

edit_profile = Blueprint("edit_profile", __name__)

@edit_profile.route("/edit_profile", methods=["GET", "POST"])
def edit_profile_page():
    if "user_id" not in session:
        flash("Please login first")
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        
        connection = sqlite3.connect("arbor_db.db")
        connection.row_factory = sqlite3.Row  
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM profile WHERE user_id = ?", (session["user_id"],))
        existing = cursor.fetchone()

        # Always grab form values first
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        email_1 = request.form.get("email_1", "").strip()
        email_2 = request.form.get("email_2", "").strip()
        mobile_no_1 = request.form.get("mobile_no_1", "").strip()
        mobile_no_2 = request.form.get("mobile_no_2", "").strip()
        whatsapp = request.form.get("whatsapp", "").strip()
        facebook = request.form.get("facebook", "").strip()
        instagram = request.form.get("instagram", "").strip()
        twitter = request.form.get("twitter", "").strip()
        linkedin = request.form.get("linkedin", "").strip()
        youtube = request.form.get("youtube", "").strip()
        github = request.form.get("github", "").strip()
        tiktok = request.form.get("tiktok", "").strip()
        pinterest = request.form.get("pinterest", "").strip()

        if existing:
            # Use fallback to existing values if form is empty
            name        = name or None
            description = description or None
            email_1     = email_1 or None
            email_2     = email_2 or None
            mobile_no_1 = mobile_no_1 or None
            mobile_no_2 = mobile_no_2 or None
            whatsapp    = whatsapp or None
            facebook    = facebook or None
            instagram   = instagram or None
            twitter     = twitter or None
            linkedin    = linkedin or None
            youtube     = youtube or None
            github      = github or None
            tiktok      = tiktok or None
            pinterest   = pinterest or None

            cursor.execute("""
                UPDATE profile
                SET name=?, description=?, email_1=?, email_2=?, mobile_no_1=?, mobile_no_2=?, whatsapp=?, facebook=?, instagram=?, twitter=?, linkedin=?, youtube=?, github=?, tiktok=?, pinterest=?
                WHERE user_id=?
            """, (name, description, email_1, email_2, mobile_no_1, mobile_no_2, whatsapp, facebook, instagram, twitter, linkedin, youtube, github, tiktok, pinterest, session["user_id"]))
        else:
            cursor.execute("""
                INSERT INTO profile(name, description, email_1, email_2, mobile_no_1, mobile_no_2, whatsapp, facebook, instagram, twitter, linkedin, youtube, github, tiktok, pinterest, user_id)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, description, email_1, email_2, mobile_no_1, mobile_no_2, whatsapp, facebook, instagram, twitter, linkedin, youtube, github, tiktok, pinterest, session["user_id"]))


        connection.commit()
        connection.close()
        flash("Profile Updated Successfully ✅")
        return redirect(url_for("dashboard.dashboard_page"))
    
    with sqlite3.connect("arbor_db.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM profile WHERE user_id = ?", (session["user_id"],))
        values = cursor.fetchone()

    return render_template("dashboard/edit_profile.html", values=values)