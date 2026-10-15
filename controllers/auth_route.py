from app import app
from flask import render_template,request,url_for,redirect,session,flash
from flask_login import login_user, logout_user, login_required
from controllers.model import User,Staff
from controllers.database import db
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Please enter username and password.", "danger")
            return render_template("login.html")

        find1 = User.query.filter_by(username=username).first()

        if not find1:
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

        # Password Verification
        if not check_password_hash(find1.password, password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

        login_user(find1)

        if find1.is_admin:
            return redirect('/admin')

        else:

            staff = Staff.query.filter_by(user_id=find1.id).first()

            if staff and staff.status == "Active":
                return redirect(url_for("staff_dashboard",staff_id=staff.id))

            flash("Your account is inactive.", "danger")
            logout_user()
            return render_template("login.html")

    return render_template("login.html")
           


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))