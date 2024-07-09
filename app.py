from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/select-main-category")
def select_main_category():
    return render_template("select_main_category.html")

@app.route("/select-sub-category")
def select_sub_category():
    return render_template("select_sub_category.html")

@app.route("/quiz/<id>")
def quiz(id):
    return render_template("quiz.html")

@app.route("/answer/<id>")
def answer(id):
    return render_template("answer.html")

@app.route("/result")
def result():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)