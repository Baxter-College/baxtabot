import datetime
import random
import json
import requests

from environment import *

import models
import message

# ==== Reset Bot ==== #
def resetBot():
	# Ensure that we are not doing J&D
	message.bot.set_variable('jd', None) # setting to none == delete the variable from bot
	message.bot.set_variable('jd_loc', None)

# ====== Specific functions ===== #
def findMeal(message):
	if ("dinner" in message):
		meal = "dinner"
	elif ("lunch" in message):
		meal = "lunch"
	elif ("breakfast" in message):
		meal = "breakfast"

	return meal

def findTime(message):

	addTime = None

	today = datetime.datetime.today() + datetime.timedelta(hours=10)
	days = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}

	if ("tomorrow" in message or "tommorow" in message):
		addTime = datetime.timedelta(hours=24)

	for day in days:
		if day in message: # if the day is mentioned
			dayDiff = days[day] - today.weekday() # get difference between days
			if dayDiff < 0: # if the day is "behind" current day, make day next week
				dayDiff += 7

			addTime = datetime.timedelta(hours=24*dayDiff)


	return addTime


def dinoRequest(meal, addTime):
	# meal is "dinner", "lunch" or "breakfast"

	ten_hours = datetime.timedelta(hours=10)

	today = datetime.datetime.now()

	today_AEST = today + ten_hours

	if (addTime):
		today_AEST += addTime

	print("Date is: {}".format(today_AEST.date().strftime('%Y-%m-%d')))

	try:
		dino = models.Meal.select().where(models.Meal.date == today_AEST.date()).where(models.Meal.type == meal).get()
	except Exception as e:
		print("---> ", e)
		print('Meal: ', meal)
		print('Date: ', today_AEST.date())
		return "Honestly.... I don't know. Go yell at my creator."

	return "{} at dino is:\n{}".format(meal, dino.description)

def dinoVote():
	return {
		"attachment": {
      		"type":"template",
      		"payload":{
        		"template_type":"button",
        		"text": "What was dino like this time?",
        		"buttons":[
          			{
            			"type":"postback",
            			"title": "Dino was great! 😋",
						"payload": "goodvote"
          			},
					{
            			"type":"postback",
            			"title": "Dino was awful! 🤢",
						"payload": "badvote"
          			}
        ]
      }
    }
	}

def makeDinoVote(vote):

	dino = getCurrentDino()

	if vote == "goodvote":
		print("the meal has: {} likes".format(dino.likes))
		dino.likes = dino.likes + 1
	elif vote == "badvote":
		print("the meal has: {} likes".format(dino.dislikes))
		dino.dislikes = dino.likes + 1

	dino.save()

def dinoPoll():

	dino = getCurrentDino()

	if (dino.likes == 0 and dino.dislikes == 0):
		message = "No one has voted! 😢\nYou can be the first to vote with 'dinovote'"

	elif (dino.likes < dino.dislikes):
		perc = (dino.dislikes / (dino.dislikes + dino.likes)) * 100
		message = "{}% of people disliked dino.".format(perc)

	elif (dino.likes > dino.dislikes):
		perc = (dino.likes / (dino.dislikes + dino.likes)) * 100
		message = "{}% of people enjoyed dino!!!".format(perc)

	else:
		message = "The crowd is split! Dino is a polarising meal.\nLet me know your thoughts with 'dinovote'"

	return {"text": message}

def getCurrentDino():

	time = datetime.datetime.now() + datetime.timedelta(hours=10) # to make it aest

	today = datetime.datetime.today() + datetime.timedelta(hours=10)
	breakfast = today.replace(hour=10, minute=0)
	lunch = today.replace(hour=14, minute=0)
	dinner = today.replace(hour=23, minute=59) # just to make sure

	if (time < breakfast):
		# for today's breakfast
		dino = models.Meal.select().where(models.Meal.type == "breakfast").where(models.Meal.date == today.date()).get()
	elif (time < lunch):
		# for today's lunch
		dino = models.Meal.select().where(models.Meal.type == "lunch").where(models.Meal.date == today.date()).get()
	elif (time < dinner):
		# for today's dinner
		dino = models.Meal.select().where(models.Meal.type == "dinner").where(models.Meal.date == today.date()).get()

	return dino


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
		message.bot.set_variable('jd', None)
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

# ===== Baxter Events ===== #

def uploadAsset(assetUrl):

	r = requests.post(
		"https://graph.facebook.com/v2.6/me/message_attachments",
		params = { "access_token": PAGE_ACCESS_TOKEN },
		json = {
			"message":{
			    "attachment":{
			     	"type":"image",
			     	"payload":{
			        	"is_reusable": True,
			        	"url": assetUrl
			      	}
			    }
			 }
		}
	)

	if (r.status_code == 200):
		return r.json()
	else:
		print("Asset Upload has gone to shit -> ", r.status_code)
		return None


def getWeekEvents(sender_psid):

	today = datetime.date.today()
	# Take todays date. Subtract the number of days which already passed this week (this gets you 'last' monday).
	week_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)


	try:
		weekCal = models.WeekCal.select().where(models.WeekCal.week_start == week_monday).get()

		message.sendAsset(sender_psid, weekCal.assetID, "image")
	except:
		message = {"text": "yeah I don't know that shit. Go yell at Tom."}
		message.callSendAPI(sender_psid, message)


# ===== Coffee Night Excuse Generator ===== #

class MarkovGenerator():

	def __init__(self, n, max):
		self.n = n # length of each ngram
		self.max = max # maximum amount to generate
		self.ngrams = {}
		self.beginnings = []

	def feed(self, text):

		if (len(text) < self.n):
			return False # discard line if it's too short

		beginning = text[0:self.n] # store the first ngram of the line
		self.beginnings.append(beginning)

		for i in range(len(text) - self.n):
			gram = text[i:i+self.n]
			next = text[i + self.n]

			# if the ngram does not already exist
			if (gram not in self.ngrams):
				self.ngrams[gram] = []

			# add to list
			self.ngrams[gram].append(next)

	def generate(self):

		# get random beginning
		current = random.choice(self.beginnings)
		output = current

		# generate new token max number of times
		for i in range(self.max):
			if current in self.ngrams:
				# all possible next tokens
				possible_next = self.ngrams[current]

				# pick one randomly
				next = random.choice(possible_next)

				output += next

				current = output[len(output) - self.n : len(output)]
			else:
				break

		# here's what we got!
		return output

def generate_excuse(rs, args):
	lines = [
		"dearest xanthe please accept my sincerest apologies",
		"please excuse me for my inability to make it to coffee night",
		"dear xanthe I am unable to attend coffee night as I am at dinner with my family",
		"I am unable to make it to coffee night as I am currently with my Nan in my hometown",
		"Dear Xanthe...I have grown very unwell thus far and hence will not be coming to coffee night #sorrynotsorry",
		"I CAN'T MAKE IT",
		"UNABLE TO BE THERE!",
		"Soz Xath. There ain't no way I'm making to to coff night baby."
		"Unfortunately, I have lectures and tutorials and am extremely busy and as such can not make it to coffee night sorry!"
	]

	markov = MarkovGenerator(3, 1500)

	for line in lines:
		markov.feed(line)

	return markov.generate()
