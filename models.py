import datetime
import psycopg2
import os
import urlparse

from peewee import *

if 'HEROKU' in os.environ:
	url = urlparse.urlparse(os.environ["DATABASE_URL"])
db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
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
