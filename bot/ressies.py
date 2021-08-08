from bot.models import Ressie, Client
import csv
import bot.functions as functions
from io import StringIO

def ressie_create(first_name, last_name, room_number):
    '''
    Creates a new resident

    Parameters:
    - first_name
    - last_name
    - room_number

    Exceptions:
    - InputError: len(first_name) < 2 or len(first_name) > 20
    - InputError: len(last_name) < 2 or len(last_name) > 20
    - InputError: room number < 0
    '''
    Ressie.create(
        first_name = first_name,
        last_name = last_name,
        room_number = room_number,
        floor = int(str(room_number)[:1])
        )  # get the first digit of the room number and set that as floor

def ressie_delete(ressie_id):
    '''
    Deletes the resident with the specified id

    Exceptions:
    - InputError: no ressie exists with that id
    '''
    ressie = Ressie.select().where(Ressie.id == ressie_id).get()
    ressie.delete_instance()

def ressies_all():
    ressies = Ressie.select(Ressie.id, Ressie.first_name, Ressie.last_name, Ressie.room_number, Ressie.floor, Ressie.college,
                        Client.dietaries).join(Client).dicts()

    return ressies

def file_upload(file):
    # Delete all ressie currently in the DB
    '''
    ressies = Ressie.select()
    for ressie in ressies:
        ressie.delete_instance()
    '''

    # Read through the CSV and create new Ressie entries
    FILE = StringIO(file.read().decode('utf-8'))
    reader = csv.reader(FILE)
    next(reader, None)

    for row in reader:
        first_name, last_name, room_number = functions.extractRessieFromCSV(row)
        ressie_create(first_name, last_name, room_number)
