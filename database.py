from peewee import *
import datetime
from flask_login import UserMixin

db = SqliteDatabase("exam_passer_app.db")

class BaseModel(UserMixin,Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
    deleted_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True

class User(BaseModel):

    username = CharField(unique=True)
    password= CharField()

    class Meta:
        database = db

class MainCategory(BaseModel):
    name = CharField()

    class Meta:
        database = db

class Answer(BaseModel):
    name= CharField()

    class Meta:
        database = db

class Question(BaseModel):
    year = IntegerField()
    main_category_id = ForeignKeyField(MainCategory)
    content = CharField()
    answer_id = ForeignKeyField(Answer)

    class Meta:
        database = db

class Result(BaseModel):
    user_id = ForeignKeyField(User)
    question_id = ForeignKeyField(Question)
    my_answer = CharField()
    result = CharField()

    class Meta:
        database = db

class Group(BaseModel):
    name = CharField()

    class Meta:
        database = db

class UserGruop(BaseModel):
    group_id = ForeignKeyField(Group)
    user_id = ForeignKeyField(User)

    class Meta:
        database = db


db.create_tables([User,MainCategory,Answer,Question,Result,Group,UserGruop])