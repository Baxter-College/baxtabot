import datetime
import psycopg2
import os

from peewee import *

if 'HEROKU' in os.environ:
	db = PostgresqlDatabase(os.environ['DATABASE_URL'])
else:
	db = PostgresqlDatabase('baxtabot', user='tomhill', password='angular')

class Meal(Model):
	date = DateField()
	type = CharField()
	description = TextField()
	likes = IntegerField(default=0)
	dislikes = IntegerField(default=0)

	class Meta:
		database = db

def goGoPowerRangers():
	db.connect()
	db.create_tables([Meal], safe=True)
	db.close()
