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
    return User.get(User.id == user_id)

@app.route("/select-main-category")
def select_main_category():
    
    user = current_user
    main_category_names = MainCategory.select()
    return render_template("select_main_category.html",user=user,main_category_names=main_category_names)

@app.route("/quiz/<id>")
def quiz(id):
    page = request.args.get("page")
    datas = Question.select().where(Question.main_category_id == int(id)).order_by(fn.Random()).limit(1)
    return render_template("quiz.html",datas = datas, page=int(page))

@app.route("/answer/<id>/<answer_id>")
def answer(id,answer_id):
    id = int(id)
    answer = Question.get(Question.id == id)
    if answer.answer_id == int(answer_id):
        result = "正解"
    else:
        result = "不正解"
    print("これがデータ:" + str(answer))
    return render_template("answer.html",id=id,answer_id=answer_id,answer=answer,result=result)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create(username = username, password=password)
        return redirect(url_for('login'))
    return render_template('register.html')

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