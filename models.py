# Models.py
#
# Defines all database models that are used elsewhere

import datetime
import psycopg2
import os
from urllib.parse import urlparse

from peewee import *
from fuzzywuzzy import fuzz, process

if "HEROKU" in os.environ:
    url = urlparse(os.environ["DATABASE_URL"])
    db = PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port,
    )
else:
    db = PostgresqlDatabase(
        os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def fuzzySearch(name):
        """ Matches search by closest string, returns string match, confidence, record """
        return process.extractOne(
            name, {sender: sender.full_name for sender in Sender.select()}
        )


class WeekCal(Model):
    assetID = CharField()
    week_start = DateField()

    class Meta:
        database = db


class Ressie(Model):
    first_name = CharField()
    last_name = CharField()
    room_number = IntegerField()
    floor = IntegerField()
    college = CharField(default="baxter")  # Incase we use for the rest of TKC

    class Meta:
        database = db

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def fuzzySearch(name):
        """ Matches search by closest string, returns string match, confidence, record """
        return process.extractOne(
            name, {ressie: ressie.full_name for ressie in Ressie.select()}
        )


def goGoPowerRangers():
    db.connect()
    db.create_tables([Meal, Sender, WeekCal, Ressie], safe=True)
    db.close()
