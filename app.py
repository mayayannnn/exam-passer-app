from database import User,MainCategory,Answer,Question,Result,Group,UserGruop
from flask import Flask
from flask import render_template,redirect
from peewee import fn
from flask import request
from flask_login import LoginManager
import os

app = Flask(__name__)


# app.config['SECRET_KEY'] = os.urandom(24)
# login_manager = LoginManager()
# login_manager.init_app(app)


@app.route("/select-main-category")
def select_main_category():
    main_category_names = MainCategory.select()
    return render_template("select_main_category.html",main_category_names=main_category_names)

@app.route("/quiz/<id>")
def quiz(id):
    page = request.args.get("page")
    datas = Question.select().where(Question.main_category_id == int(id)).order_by(fn.Random()).limit(1)
    return render_template("quiz.html",datas = datas, page=int(page))

@app.route("/answer/<id>/<answer_id>")
def answer(id,answer_id):
    id = int(id)
    answer = Question.get(Question.id == id)
    if answer.answer == int(answer_id):
        result = "正解"
    else:
        result = "不正解"
    print("これがデータ:" + str(answer))
    return render_template("answer.html",id=id,answer_id=answer_id,answer=answer,result=result)

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():


    return render_template("register.html")

@app.route("/create_user",methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    User.create(username=username,password=password)
    return redirect("/select-main-category")

@app.route("/login_user",methods=["POST"])
def login_user():
    username = request.form["username"]
    password = request.form["password"]
    user = User.get(User.username == username,User.password == password)
    print(str(user.username)  + "が入った")
    return redirect("/select-main-category")

if __name__ == "__main__":
    app.run(debug=True)