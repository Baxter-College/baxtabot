# Models.py
#
# Defines all database models that are used elsewhere

import datetime
import psycopg2
import os
from urllib.parse import urlparse

from peewee import Model, PostgresqlDatabase
from peewee import DateField, CharField, BigIntegerField, DateTimeField, TextField
from peewee import IntegerField, ForeignKeyField, BooleanField
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
    db_name = os.environ["DB_NAME"]
    db_user = os.environ["DB_USER"]
    db_pword = os.environ["DB_PASSWORD"]
    db = PostgresqlDatabase(
        db_name,
        user=db_user,
        password=db_pword,
    )

class Base(Model):
    class Meta:
        database = db

class Meal(Base):
    date = DateField()
    type = CharField()
    description = TextField()
    likes = IntegerField(default=0)
    dislikes = IntegerField(default=0)

class mealOrder(Base):
    date = DateField(null=True)
    meal = CharField(null=True)
    confirmation = BooleanField(default=False)

class Sender(Base):
    psid = BigIntegerField()
    first_name = CharField()
    last_name = CharField()
    profile_url = CharField()
    last_message = DateTimeField()
    conversation = CharField(null=True, default=None)

    inloop_password = CharField(null=True, default=None)
    email = CharField(null=True, default=None)
    order = ForeignKeyField(mealOrder, backref="customer")
    askedForPassword = BooleanField(default=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def add_crush(self, other):
        Crush.create(crusher=self, crushee=other)

    def remove_crush(self, other):
        Crush.select().where(Crush.crusher == self and Crush.crushee == other)
    
    def is_crushing(self, other):
        try:
            Crush.select().where(Crush.crusher.id == self.id).where(Crush.crushee.id == other.id).get()
            return True
        except:
            return False

    @property
    def crushes(self):
        return Crush.select().where(Crush.crusher.id == self.id)

    @staticmethod
    def fuzzySearch(name):
        """ Matches search by closest string, returns string match, confidence, record """
        return process.extractOne(
            name, {sender: sender.full_name for sender in Sender.select()}
        )


class MealImg(Base):
    meal = ForeignKeyField(Meal, backref="images")
    url = TextField()
    sender = ForeignKeyField(Sender)


class Crush(Base):
    crushee = ForeignKeyField(Sender, backref="crushOf")
    crusher = ForeignKeyField(Sender, backref="crushes")


class WeekCal(Base):
    assetID = CharField()
    week_start = DateField()


class Ressie(Base):
    first_name = CharField()
    last_name = CharField()
    room_number = IntegerField()
    floor = IntegerField()
    college = CharField(default="baxter")  # Incase we use for the rest of TKC

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
    db.create_tables([Meal, Sender, WeekCal, Ressie, Crush, MealImg], safe=True)
    db.close()
