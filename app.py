from flask import Flask
from flask import render_template
# from datetime import datetime
# import re

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/upload")
def upload(name = None):
    return render_template("upload.html", name=name)