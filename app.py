from database import User,MainCategory,Answer,Question,Result,Group,UserGruop
from flask import Flask
from flask import render_template,redirect,url_for
from peewee import fn
from flask import request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))

@app.route("/select-main-category")
@login_required
def select_main_category():
    user = current_user
    main_category_names = MainCategory.select()
    return render_template("select_main_category.html",user=user,main_category_names=main_category_names)

@app.route("/quiz/<id>")
def quiz(id):
    page = request.args.get("page")
    number = 10
    if int(page) == int(number) + 1:
        return redirect(url_for("result"))
    datas = Question.select().where(Question.main_category_id == int(id)).order_by(fn.Random()).limit(1)
    return render_template("quiz.html",datas = datas, page=int(page),page2 = str(page))

@app.route("/answer/<id>/<answer_id>")
@login_required
def answer(id,answer_id):
    page = request.args.get("page")
    id = int(id)
    answer = Question.get(Question.id == id)
    if str(answer.answer_id) == str(answer_id):
        a = 1
        kekka = True
    else:
        a = 2
        kekka = False
    d = Answer.get(Answer.id == a)
    result = d.name
    # ここから下はresultの作成
    if int(answer_id) == 1:
        my_answer = True
    else:
        my_answer = False
    question_id  = answer.id
    user_id = current_user.id
    Result.create(question_id = question_id,user_id=user_id,my_answer=my_answer,result=kekka)
    return render_template("answer.html",id=id,answer_id=answer_id,answer=answer,result=result,page=int(page))

@app.route("/result")
@login_required
def result():
    datas = Result.select().where(Result.user_id == current_user.id)
    datasN = datas[-10:]
    datas = []
    datas2 = []
    for i in datasN:
        datas.append(Result.get(Result.id == i))
        datas2.append(Question.get(Question.id == Result.get(Result.id == i).question_id ))
    return render_template("result.html",datas = datas,datas2 = datas2)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create(username = username, password=password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route("/edit_user", methods=['GET', 'POST'])
@login_required
def edit_user():
    user = User.get(User.id == current_user.id)
    if request.method == "POST":
        username = request.form['username']
        password = request.form["password"]
        repassword = request.form["repassword"]
        user.username = username
        user.save()
        # ここからパスワード設定
        if user.password == password:
            user.password = repassword
            user.save()
        return redirect("/select-main-category")
    return render_template("/edit_user.html",user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get(User.username == username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('select_main_category'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)