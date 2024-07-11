from peewee import *

db = SqliteDatabase("exam_passer_app.db")

class MainCategory(Model):
    name = CharField()

    class Meta:
        database = db

class Category(Model):
    main_category_id = IntegerField()

    class Meta:
        database = db



db.create_tables([MainCategory,Category])