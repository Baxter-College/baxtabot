from bot.models import Meal

def meals_all():
    return Meal.select().order_by(Meal.date.desc())

def meals_add(date, description, type):
    models.Meal.create(
        date=date, description=description, type=type
    )

def meals_delete(meal_id):
    meal = models.Meal.select().where(models.Meal.id == meal_id).get()
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
