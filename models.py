# Models.py
#
# Defines all database models that are used elsewhere

import datetime
import psycopg2
import os
from urllib.parse import urlparse

from peewee import *

if 'HEROKU' in os.environ:
	url = urlparse(os.environ["DATABASE_URL"])
	db = PostgresqlDatabase(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
else:
	db = PostgresqlDatabase(os.environ["DB_NAME"], user=os.environ["DB_USER"], password=os.environ["DB_PASSWORD"])

class Meal(Model):
	date = DateField()
	type = CharField()
	description = TextField()
	likes = IntegerField(default=0)
	dislikes = IntegerField(default=0)

	class Meta:
		database = db

class Sender(Model):
	psid = BigIntegerField()
	first_name = CharField()
	last_name = CharField()
	profile_url = CharField()
	last_message = DateTimeField()

	class Meta:
		database = db

class WeekCal(Model):
	assetID = CharField()
	week_start = DateField()

	class Meta:
		database = db


def goGoPowerRangers():
	db.connect()
	db.create_tables([Meal, Sender, WeekCal], safe=True)
	db.close()
