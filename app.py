import os
import smtplib
import ssl
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for, flash
from db import init_db, get_conn

app = Flask(__name__)
init_db()
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-change-me")


def send_contact_email(name: str, email: str, message: str) -> None:
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]
    to_email = os.environ.get("CONTACT_TO", smtp_user)

    msg = EmailMessage()
    msg["Subject"] = f"Portfolio contact from {name}"
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Reply-To"] = email

    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}\n")

    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
        server.starttls(context=context)
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/projects")
def projects():
    return render_template("projects.html")


@app.get("/contact")
def contact():
    return render_template("contact.html")


@app.post("/contact")
def contact_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        flash("Please fill out all fields.", "error")
        return redirect(url_for("contact"))

    try:
        send_contact_email(name, email, message)
        flash("Message sent. I’ll get back to you soon.", "success")
    except Exception:
        app.logger.exception("Email send failed")
        flash("Could not send your message right now. Try again later.", "error")

    return redirect(url_for("contact"))