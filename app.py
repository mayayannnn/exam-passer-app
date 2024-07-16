from database import Category,MainCategory,answer
from flask import Flask
from flask import render_template
from peewee import fn

app = Flask(__name__)

@app.route("/select-main-category")
def select_main_category():
    main_category_ids = Category.select()
    return render_template("select_main_category.html",main_category_ids=main_category_ids)

@app.route("/quiz/<id>")
def quiz(id):
    datas = MainCategory.select().where(MainCategory.category_id == id).order_by(fn.Random()).limit(1)
    return render_template("quiz.html",datas = datas)

@app.route("/answer/<id>")
def answer(id):
    
    return render_template("answer.html",id=id)

@app.route("/result")
def result():
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)