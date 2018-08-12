import datetime

from environment import *

import models

# ====== Specific functions ===== #
def dinoRequest(message):

	if ("dinner" in message):
		meal = "dinner"
	elif ("lunch" in message):
		meal = "lunch"
	elif ("breakfast" in message):
		meal = "breakfast"

	ten_hours = datetime.timedelta(hours=10)

	today = datetime.datetime.now()

	today_AEST = today + ten_hours

	if ("tommorow" in message or "tomorrow" in message):
		today_AEST += datetime.timedelta(hours=24)

	print("Date is: {}".format(today_AEST.date().strftime('%Y-%m-%d')))

	try:
		dino = models.Meal.select().where(models.Meal.date == today_AEST.date()).where(models.Meal.type == meal).get()
	except Exception as e:
		print("---> ", e)
		print('Meal: ', meal)
		print('Date: ', today_AEST.date())
		return "Honestly.... I don't know"

	return "{} at dino is:\n{}".format(meal, dino.description)

def dinoVote():
	return {
		"text": "What dino meal was it?",
		"quick_replies": [
			{
				"content_type":"text",
        		"title":"Breakfast",
        		"payload":"dinovote breakfast"
			},
			{
				"content_type":"text",
        		"title":"Lunch",
        		"payload":"dinovote lunch"
			},
			{
				"content_type":"text",
        		"title":"Dinner",
        		"payload":"dinovote dinner"
			}

		]
	}
