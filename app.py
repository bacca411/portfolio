from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/projects")
def projects():
    return render_template("projects.html")

@app.get("/contact")
def contact():
    return render_template("contact.html")