import mammoth
from bot.models import Meal
import bot.functions as functions


def meals_all():
    '''
    Return a list of all meals
    '''
    return Meal.select().order_by(Meal.date.desc())


def meals_add(date, description, type):
    '''
    Add a new meal

    Parameters:
    - date
    - description
    - type

    Exceptions:
    - InputError: date is not valid
    - InputError: description is empty
    - InputError: type not in ['breakfast', 'lunch', 'dinner']

    Return value: None
    '''
    Meal.create(
        date=date, description=description, type=type
    )


def meals_delete(meal_id):
    '''
    Deletes an existing meal

    Paramters:
    - meal_id

    Exceptions:
    - InputError: meal_id is not valid
    '''
    meal = Meal.select().where(Meal.id == meal_id).get()
    meal.delete_instance()


def file_extract_docx(file):
    '''
    Extracts the dino menu from a .docx file

    Parameters:
    - file: a file object

    Return value:
    - Parsed dino menu
    '''
    result = mammoth.convert_to_html(file)
    html = result.value  # The generated HTML
    messages = (
        result.messages
    )  # Any messages, such as warnings during conversion

    extracted = functions.dinoparse(html)
    return extracted


def file_extract_html(file):
    '''
    Extracts the dino menu from a .html file

    Parameters:
    - File: an open file object

    Return value:
    - Parsed dino menu
    '''
    mealsByDay = functions.dinoparse(file.readlines())
    return mealsByDay
