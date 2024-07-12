from peewee import *

db = SqliteDatabase("exam_passer_app.db")

class MainCategory(Model):
    name = CharField()
    category_id = IntegerField()
    answer = IntegerField()

    class Meta:
        database = db

class Category(Model):
    main_category_id = IntegerField()

    class Meta:
        database = db

class answer(Model):
    answer_id = IntegerField()

    class Meta:
        database = db



db.create_tables([MainCategory,Category,answer])