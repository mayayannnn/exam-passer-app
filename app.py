from database import User,MainCategory,Answer,Question,Result,Group,UserGruop
from flask import Flask
from flask import render_template,redirect,url_for,flash
from peewee import fn
from flask import request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import ast

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
    questions =  Question.select(Question.year).distinct()
    main_category_names = MainCategory.select()
    return render_template("select_main_category.html",user=user,main_category_names=main_category_names,questions=questions)

@app.route("/quiz",methods=["POST"])
def quiz_post():
    user = current_user
    main_category = request.form.getlist("main_category")
    year = request.form.getlist("year")
    page = request.args.get("page")
    print(year)
    number = 10
    if int(page) == int(number) + 1:
        return redirect(url_for("result"))
    datas = Question.select().where(Question.main_category_id.in_(main_category) & Question.year.in_(year)).order_by(fn.Random()).limit(1)
    return render_template("quiz.html",user=user,datas = datas, page=int(page),page2 = str(page),main_category=main_category,year=year)


@app.route("/answer/<id>/<answer_id>/<main_category>/<year>",methods=["POST"])
@login_required
def answer(id,answer_id,main_category,year):
    user = current_user
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
    return render_template("answer.html",user = user,id=id,answer_id=answer_id,answer=answer,result=result,page=int(page),main_category=ast.literal_eval(main_category),year=ast.literal_eval(year))

@app.route("/result")
@login_required
def result():
    datas = Result.select().where(Result.user_id == current_user.id)
    number = 10
    datasN = datas[-number:]
    datas = []
    datas2 = []
    for i in datasN:
        datas.append(Result.get(Result.id == i))
        datas2.append(Question.get(Question.id == Result.get(Result.id == i).question_id ))
    return render_template("result.html",datas = datas,datas2 = datas2,number = int(number))

@app.route("/result_all/<id>")
@login_required
def result_all(id):
    # user_groups = UserGruop.select().where(UserGruop.user_id == int(id))
    # groups = []
    # user_groups = []
    # users = []
    # for user_group in user_groups:
    #     groups.append(Group.get(Group.id == user_group.group_id))
    # for group in groups:
    #     user_groups.append(UserGruop.get(UserGruop.id == group.id))
    # for user_group in user_groups:
    #     users.append(User.get(User.id == user_group.user_id))
    # print("これがデータ:" + str(user_groups))
    if int(id) == current_user.id:
        datas = Result.select().where(Result.user_id == int(id))
        questions = []
        categorys = []
        number = len(datas)
        for data in datas:
            question = Question.get(Question.id == data.question_id)
            questions.append(question)
        for question in questions:
            category = MainCategory.get(MainCategory.id == question.main_category_id)
            categorys.append(category)
    else:
        return redirect(url_for("select-main-category"))
    return render_template("/result_all.html",datas = datas,questions = questions,number = number,categorys = categorys)


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
            flash("パスワードを変更しました")
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
            flash(f"ようこそ{username}さん")
            return redirect(url_for('select_main_category'))
        else:
            flash("パスワードかユーザー名を間違っています")
            print("hello")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("ログアウトしました")
    return redirect(url_for('login'))

@app.route("/group")
@login_required
def group():
    user = current_user
    user_groups = UserGruop.select().where(UserGruop.user_id == int(current_user.id))
    groups = []
    for user_group in user_groups:
        groups.append(Group.get(id = user_group.id))
    return render_template("group.html",groups = groups,user=user)

@app.route("/add_group",methods=['GET', 'POST'])
@login_required
def add_group():
    user = current_user
    if request.method == "POST":
        name = request.form["name"]
        Group.create(name = name)
        group = Group.get(Group.name == name)
        UserGruop.create(group_id = group.id,user_id = current_user.id)
        return redirect(url_for("group"))
    return render_template("add_group.html",user=user)

@app.route("/detail_group/<id>")
def detail_group(id):
    user = current_user
    user_groups = UserGruop.select().where(UserGruop.group_id == id)
    users = []
    for user_group in user_groups:
        users.append(User.get(id = user_group.user_id))
    return render_template("/detail_group.html",users=users,user = user,id = id)

@app.route("/add_member",methods=["POST"])
def add_member():
    username = request.form["username"]
    group_id = request.form["group"]
    user_id = User.get(User.username == username)
    UserGruop.create(user_id = user_id, group_id = group_id)
    flash("グループに新しいメンバーを追加しました")
    return redirect(f"/detail_group/{group_id}")

if __name__ == "__main__":
    app.run(debug=True)