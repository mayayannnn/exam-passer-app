from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/select-main-category")
def select_main_category():
    return render_template("select_main_category.html")

if __name__ == "__main__":
    app.run(debug=True)