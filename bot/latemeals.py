from bot.models import LateMeal, Ressie, Meal, Client

def latemeals_oustanding():
    oustanding_meals = LateMeal.select(LateMeal.id, Ressie.first_name, Ressie.last_name,
                        Meal.date, Meal.type, Meal.description, Client.dietaries).join(Ressie).join(Client).switch(LateMeal).join(Meal).where(LateMeal.completed == 0).dicts()

    return oustanding_meals

def latemeals_completed():
    completed_meals = LateMeal.select(LateMeal.id, Ressie.first_name, Ressie.last_name,
                        Meal.date, Meal.type, Meal.description, Client.dietaries).join(Ressie).join(Client).switch(LateMeal).join(Meal).where(LateMeal.completed == 1).dicts()

    return completed_meals

def latemeal_delete(meal_id):
    meal = LateMeal.select().where(LateMeal.id == meal_id).get()
    meal.delete_instance()

def latemeals_setcompleted(latemealid):
    query = LateMeal.update(completed=True).where(LateMeal.id == latemealid)
    query.execute()

def latemeals_oustanding_resident(client_id):
    oustanding_meals = LateMeal.select(LateMeal.id, Meal.date, Meal.type, Meal.description).join(Ressie).join(Client).switch(LateMeal).join(Meal).where((LateMeal.completed == 0) & (Client.id == client_id)).dicts()
    return oustanding_meals
