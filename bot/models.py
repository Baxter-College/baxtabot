# Models.py
#
# Defines all database models that are used elsewhere

import datetime
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
    # db_name = os.environ["DB_NAME"]
    # db_user = os.environ["DB_USER"]
    # db_pword = os.environ["DB_PASSWORD"]
    db = SqliteDatabase(
        'test.db',
        pragmas={
            'foreign_keys': 'on'
        }
    )

class BaxtabotEntity(Model):
    class Meta:
        database = db


class Meal(BaxtabotEntity):
    date = DateField()
    type = CharField()
    description = TextField()
    likes = IntegerField(default=0)
    dislikes = IntegerField(default=0)

class Sender(BaxtabotEntity):
    psid = BigIntegerField()
    first_name = CharField()
    last_name = CharField()
    profile_url = CharField()
    last_message = DateTimeField()
    conversation = CharField(null=True, default=None)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def add_crush(self, other):
        Crush.create(crusher=self, crushee=other)

    def remove_crush(self, other):
        Crush.select.where(Crush.crusher == self and Crush.crushee == other)

    @property
    def crushes(self):
        return Crush.select().where(Crush.crusher.id == self.id)

    @staticmethod
    def fuzzySearch(name):
        """ Matches search by closest string, returns string match, confidence, record """
        return process.extractOne(
            name, {sender: sender.full_name for sender in Sender.select()}
        )

class MealImg(BaxtabotEntity):
    meal = ForeignKeyField(Meal, backref="images")
    url = TextField()
    sender = ForeignKeyField(Sender)

class Crush(BaxtabotEntity):
    crushee = ForeignKeyField(Sender, backref="crushOf")
    crusher = ForeignKeyField(Sender, backref="crushes")

class WeekCal(BaxtabotEntity):
    assetID = CharField()
    week_start = DateField()

class Ressie(BaxtabotEntity):
    first_name = CharField()
    last_name = CharField()
    room_number = IntegerField()
    floor = IntegerField()
    college = CharField(default="baxter")  # Incase we use for the rest of TKC
    # facebook_psid = BigIntegerField()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def fuzzySearch(name):
        """ Matches search by closest string, returns string match, confidence, record """
        dic = {ressie: ressie.full_name for ressie in Ressie.select()}
        print("fuxxdic", dic)
        outp = process.extractOne(
            name, dic
        )
        print("fuzzy output ", outp)
        return outp


class LateMeal(BaxtabotEntity):
    meal = ForeignKeyField(Meal)
    ressie = ForeignKeyField(Ressie)
    notes = TextField()
    completed = BooleanField()

class Client(BaxtabotEntity):
    email = TextField()
    password = TextField()
    position = TextField(default='')
    name = TextField()
    ressie = ForeignKeyField(Ressie, null=True)
    dietaries = TextField(default='None')
    roomshown = BooleanField(default=False)

class ClientPermissions(BaxtabotEntity):
    client = ForeignKeyField(Client)
    dinoread = BooleanField(default=True)
    dinowrite = BooleanField(default=False)
    calendar = BooleanField(default=False)
    ressies = BooleanField(default=False)
    latemeals = BooleanField(default=False)
    sport = BooleanField(default=False)
    users = BooleanField(default=False)

class ActiveTokens(BaxtabotEntity):
    client = ForeignKeyField(Client)
    token = TextField()

def goGoPowerRangers():
    db.connect()
    db.create_tables([Meal, Sender, WeekCal, Ressie, Crush, MealImg, LateMeal, Client, ClientPermissions, ActiveTokens], safe=True)
    db.close()
