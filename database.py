from peewee import *

db = SqliteDatabase("exam_passer_app.db")

class User(Model):
    username = CharField()
    password= CharField()

    class Meta:
        database = db

class MainCategory(Model):
    name = CharField()

    class Meta:
        database = db

class Answer(Model):
    name= CharField()

    class Meta:
        database = db

class Question(Model):
    year = IntegerField()
    main_category_id = IntegerField()
    content = CharField()
    answer_id = IntegerField()

    class Meta:
        database = db

class Result(Model):
    user_id = IntegerField()
    question_id = IntegerField()
    result = CharField()

    class Meta:
        database = db

class Group(Model):
    name = CharField()

    class Meta:
        database = db

class UserGrop(Model):
    group_id = IntegerField()
    user_id = IntegerField()

    class Meta:
        database = db


db.create_tables([User,MainCategory,Answer,Question,Result,Group,UserGrop])