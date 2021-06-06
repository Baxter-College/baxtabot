from bot.models import LateMeal, Ressie, Meal, Client

def latemeals_oustanding():
    '''
    Returns a list of all outstanding late meals

    Columns returned:
    - id
    - firstname + lastname of ressie
    - date
    - meal type (b, l, d)
    - meal description
    - dietary requirements of ressie
    '''
    oustanding_meals = LateMeal.select(LateMeal.id, Ressie.first_name, Ressie.last_name,
                        Meal.date, Meal.type, Meal.description, Client.dietaries).join(Ressie).join(Client).switch(LateMeal).join(Meal).where(LateMeal.completed == 0).dicts()

    return oustanding_meals

def latemeals_completed():
    '''
    Returns a list of all completed late meals

    Columns returned:
    - id
    - firstname + lastname of ressie
    - date
    - meal type (b, l, d)
    - meal description
    - dietary requirements of ressie
    '''
    completed_meals = LateMeal.select(LateMeal.id, Ressie.first_name, Ressie.last_name,
                        Meal.date, Meal.type, Meal.description, Client.dietaries).join(Ressie).join(Client).switch(LateMeal).join(Meal).where(LateMeal.completed == 1).dicts()

    return completed_meals

def latemeal_delete(meal_id):
    meal = LateMeal.select().where(LateMeal.id == meal_id).get()
    meal.delete_instance()

def latemeals_setcompleted(latemealid):
    '''
    Marks a late meal as completed

    Parameters: latemeal_id

    Exceptions:
    - InputError: latemeal_id is not valid
    '''
    query = LateMeal.update(completed=True).where(LateMeal.id == latemealid)
    query.execute()

def latemeals_oustanding_resident(client_id):
    '''
    Returns a list of all completed late meals for a particular client

    Exceptions:
    - InputError: client_id is not valid

    Columns returned:
    - id
    - firstname + lastname of ressie
    - date
    - meal type (b, l, d)
    - meal description
    - dietary requirements of ressie
    '''
    oustanding_meals = LateMeal.select(LateMeal.id, Meal.date, Meal.type, Meal.description).join(Ressie).join(Client).switch(LateMeal).join(Meal).where((LateMeal.completed == 0) & (Client.id == client_id)).dicts()
    return oustanding_meals
