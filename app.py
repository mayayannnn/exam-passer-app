from database import Category,MainCategory,answer
from flask import Flask
from flask import render_template
from peewee import fn
from flask import request

app = Flask(__name__)
page = 0


@app.route("/select-main-category")
def select_main_category():
    main_category_ids = Category.select()
    return render_template("select_main_category.html",main_category_ids=main_category_ids)

@app.route("/quiz/<id>")
def quiz(id):
    page = request.args.get("page")
    datas = MainCategory.select().where(MainCategory.category_id == id).order_by(fn.Random()).limit(1)
    return render_template("quiz.html",datas = datas, page=int(page))

@app.route("/answer/<id>/<answer_id>")
def answer(id,answer_id):
    id = int(id)
    answer = MainCategory.get(MainCategory.id == id)
    if answer.answer == int(answer_id):
        result = "正解"
    else:
        result = "不正解"
    print("これがデータ:" + str(answer))
    return render_template("answer.html",id=id,answer_id=answer_id,answer=answer,result=result)

@app.route("/result")
def result():
    print("page=", page)
    return render_template(
        "result.html",
    )

if __name__ == "__main__":
    app.run(debug=True)