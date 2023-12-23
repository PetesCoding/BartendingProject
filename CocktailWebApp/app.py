#!usr/bin/env python3

from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/bar")
def bar():
    return render_template("bar.html")


@app.route("/ingredients")
def ingredients():
    return render_template("ingredients.html")


@app.route("/cocktails")
def cocktails():
    return render_template("cocktails.html")


@app.route("/popular")
def popular():
    return render_template("popular.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=3000, debug=True)