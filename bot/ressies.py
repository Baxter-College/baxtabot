from bot.models import Ressie
import csv
from io import StringIO

def ressie_create(first_name, last_name, room_number):
    Ressie.create(
        first_name = first_name,
        last_name = last_name,
        room_number = room_number,
        floor = int(str(room_number)[:1])
        )  # get the first digit of the room number and set that as floor

def ressie_delete(ressie_id):
    ressie = models.Ressie.select().where(models.Ressie.id == ressie_id).get()
    ressie.delete_instance()

def ressies_all():
    return Ressie.select()

def file_upload():
    # Delete all ressie currently in the DB
    ressies = models.Ressie.select()
    for ressie in ressies:
        ressie.delete_instance()

    # Read through the CSV and create new Ressie entries
    FILE = StringIO(file.read().decode('utf-8'))
    reader = csv.reader(FILE)
    next(reader, None)

    for row in reader:
        first_name, last_name, room_number = functions.extractRessieFromCSV(row)
        ressie_create(first_name, last_name, room_number)
