from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
import random
from flask import current_app

from extensions import db, bcrypt, mail
from models.user import User

auth = Blueprint("auth", __name__)

# Temporary OTP store (in-memory)
otp_store = {}


# ================= HOME =================
@auth.route("/")
def home():
    return redirect("/login")


# ================= REGISTER =================
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect("/register")

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        otp_store[email] = {
            "otp": otp,
            "name": name,
            "password": generate_password_hash(password)
        }

        # Send OTP email
        msg = Message(
            "Your OTP for Mail",
            sender=("Mail", current_app.config["MAIL_USERNAME"]),
            recipients=[email]
        )
        msg.body = f"Your OTP is: {otp}"
        mail.send(msg)

        session["otp_email"] = email
        return redirect("/verify-otp")

    return render_template("register.html")


# ================= VERIFY OTP =================
@auth.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    email = session.get("otp_email")

    if not email:
        return redirect("/register")

    if request.method == "POST":
        user_otp = request.form["otp"]

        if email in otp_store and otp_store[email]["otp"] == user_otp:
            data = otp_store[email]

            user = User(
                name=data["name"],
                email=email,
                password=data["password"]
            )

            db.session.add(user)
            db.session.commit()

            del otp_store[email]
            session.pop("otp_email", None)

            flash("Registration successful. Please login.")
            return redirect("/login")

        flash("Invalid OTP")

    return render_template("verify_otp.html")


# ================= LOGIN =================
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/dashboard")

        flash("Invalid email or password")

    return render_template("login.html")


# ================= LOGOUT =================
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
