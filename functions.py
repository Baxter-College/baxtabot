import datetime

from environment import *

import models
import message

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

# ======== J&D ========== #

def set_jd(rs, switch):

	jd_desc = ""

	try:
		if switch[1]:
			message.bot.set_variable('jd_loc', switch[1])
			jd_desc = " in the {}".format(switch[1])
	except:
		message.bot.set_variable('jd_loc', None)

	if switch[0].lower() == 'on':
		message.bot.set_variable('jd', True)
		# jd = True
		return "COFFEE TIME!!! ☕️\nJ&D is ON" + jd_desc
	else:
		message.bot.set_variable('jd', False)
		message.bot.set_variable('jd_loc', None)
		return "No more coff! 😭"

def get_jd(rs, args):

	jd = message.bot.get_variable('jd')
	jd_loc = message.bot.get_variable('jd_loc')

	jd_desc = ""

	if jd_loc:
		jd_desc = " in the {}".format(jd_loc)

	if jd:
		return "J&D is ON" + jd_desc
	else:
		return "J&D is OFF 😭 😭 😭"
