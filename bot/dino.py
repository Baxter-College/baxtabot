import mammoth
from bot.models import Meal
import bot.functions as functions

def meals_all():
    return Meal.select().order_by(Meal.date.desc())

def meals_add(date, description, type):
    Meal.create(
        date=date, description=description, type=type
    )

def meals_delete(meal_id):
    meal = Meal.select().where(Meal.id == meal_id).get()
    meal.delete_instance()

def file_extract_docx(file):
    result = mammoth.convert_to_html(file)
    html = result.value  # The generated HTML
    messages = (
        result.messages
    )  # Any messages, such as warnings during conversion

    extracted = functions.dinoparse(html)
    return extracted

def file_extract_html(file):
    mealsByDay = functions.dinoparse(file.readlines())
