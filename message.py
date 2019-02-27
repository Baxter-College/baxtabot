# Message.py
#
# Functionality that involves connecting and sending messages to
# the facebook Send API

import json
import requests
import datetime

from rivescript import RiveScript

from settings import *

import functions
import models

# ==== rivescript bot setup ==== #

bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()

# ==== rivescript subroutines ==== #

# These functions can be used in the rivescript documents
bot.set_subroutine("set_jd", functions.set_jd)
bot.set_subroutine("get_jd", functions.get_jd)
bot.set_subroutine("set_shop", functions.set_shop)
bot.set_subroutine("get_shop", functions.get_shop)
bot.set_subroutine("generate_excuse", functions.generate_excuse)

# ==== message handling ==== #

# here is some code

# added some more code to new feature

# Some different code
# with some different lines
#
#
#
#

#
# A heap
#
# Of code

def handleMessage(sender_psid, received_message):
	"""
	Handles a plain message request and determines what to do with it
	By word matching the content and sender_psid
	"""

	print("HANDLING MESSAGE!")
	# response = {"text": "Hi. I'm on holiday. I'm not working at the moment. I will be working again after N-Week. Message me then, and expect AMAZING new pieces of functionality!!!\n\nSee you next year!"}
	response = {}
	received_message = received_message.lower()

	# Note: should really come up with a better method to do all of this!
	if ("dinner" in received_message or "lunch" in received_message or "breakfast" in received_message):
		meal = functions.findMeal(received_message)
		addTime = functions.findTime(received_message)
		response = {
			"text": functions.dinoRequest(meal, addTime),
			"quick_replies":[
				{
	        		"content_type":"text",
	        		"title":"What's dino like?",
					"payload":"What's dino like?"
				},
				{
	        		"content_type":"text",
	        		"title":"dinovote",
					"payload":"dinovote"
				}
			]

		}

	elif ("dinopoll" in received_message or "dino like" in received_message or "dino good" in received_message):
		response = functions.dinoPoll()

	elif ("what's dino" in received_message or "what’s dino" in received_message or "what is dino" in received_message or "what's for dino" in received_message or "for dino" in received_message or "whats dino" in received_message ):
		meal = functions.getCurrentDino()
		addTime = functions.findTime(received_message)
		response = {
			"text": functions.dinoRequest(meal.type, addTime),
			"quick_replies":[
				{
	        "content_type":"text",
	        "title":"What's dino like?",
					"payload":"What's dino like?"
				},
				{
	        "content_type":"text",
	        "title":"dinovote",
					"payload":"dinovote"
				}
			]
		}

	elif ("what's on" in received_message or "what’s on" in received_message or "what is on" in received_message or "event" in received_message or "calendar" in received_message):
		functions.getWeekEvents(sender_psid) # bit weird, this one will send an asset. so break and return OK now.
		return 'OK'

	elif ("nudes" in received_message or "noods" in received_message):
		functions.nudes(sender_psid)
		return "OK"

	elif ("date" in received_message or "time" in received_message):
		response = {"text": "The date is: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))}

	elif ("dino is shit" in received_message or "dino is bad" in received_message or "dino is good" in received_message or "dinovote" in received_message or "vote" in received_message):
		response = functions.dinoVote()

	elif ("dino" in received_message):
		response = {
			"text": "You can ask me things about dino.\nLike 'What's for dinner?'\nor 'What is dino like'\nor 'dinovote' to give your opinion on dino",
			"quick_replies":[
				{
					"content_type":"text",
					"title":"What's dino?",
					"payload":"What's dino?"
				},
				{
					"content_type":"text",
					"title":"What is dino like",
					"payload":"What is dino like"
				},
				{
					"content_type":"text",
					"title":"dinovote",
					"payload":"dinovote"
				}
			]
		}

	elif ("days left" in received_message or "semester" in received_message):
		response = { "text": functions.semesterResponse()}

	elif ("room is" in received_message):
		name = functions.extractName(received_message)
		response = { "text": functions.getRoomNumber(name) }
		# response = {"text": "I don't know room numbers yet ... will be working shortly"}
		#response = {"text": "I can't assist a murder!!! My room number function has been disabled for assassin's week. Watch your back."}

	else:
		reply = bot.reply(str(sender_psid), received_message)
		response = {"text": "{}".format(reply)}

	print("Sending back: ")
	print(response)

	callSendAPI(sender_psid, response)

	return 'OK'

def handlePostback(sender_psid, received_postback):
	"""
	Handles a postback request to the webhook and determines what
	functionality / response to call
	"""

	print('RECEIVED POSTBACK: ', received_postback)

	if (received_postback['payload'] == 'goodvote'):
		response = {"text": "Sounds like a nice meal!"}
		functions.makeDinoVote("goodvote")

	elif (received_postback['payload'] == 'badvote'):
		response = {"text": "Too bad it was gross :("}
		functions.makeDinoVote("badvote")

	else:
		response = {"text": "[DEBUG] Received postback for some reason..."}

	callSendAPI(sender_psid, response)

	return 'OK'

def callSendAPI(sender_psid, response):
	"""
	Sends the response to sender via facebook Send API
	"""

	print(bot.get_uservars(str(sender_psid)))

	r = requests.post(
		"https://graph.facebook.com/v2.6/me/messages",
		params = { "access_token": PAGE_ACCESS_TOKEN },
		json = {
			"messaging_type": "RESPONSE", # alternatively MESSAGE_TAG
			"recipient": {
				"id": sender_psid
			},
			"message": response
		}
	)

	if (r.status_code == 200):
		print("sent message to meatbag!")
		return "Sent message to meatbag!"
	else:
		print("It's all gone to shit! -> ", r.status_code)
		return "It's all gone to shit", r.status_code

def sendBubbles(sender_psid):
	"""
	Sends bubbles to sender
	TODO: Include timing so bubbles don't hang around for ages
	"""

	r = requests.post(
		"https://graph.facebook.com/v2.6/me/messages",
		params = { "access_token": PAGE_ACCESS_TOKEN },
		json = {
			"recipient": {
				"id": sender_psid
			},
			"sender_action":"typing_on"
		}
	)

	if (r.status_code == 200):
		return "OK"
	else:
		print("It's all gone to shit! -> ", r.status_code)
		return "It's all gone to shit", r.status_code

def sendAsset(sender_psid, assetID, type):
	"""
	Sends an asset to sender

	Args:
		sender_psid (str): the psid of the target sender
		assetID (str): the facebook assetID obtained from uploadAsset()
		type (str): <"image"|"audio">
	"""

	message = {
		"attachment":{
			"type": type,
			"payload":{
				"attachment_id": str(assetID)
			}
		}
	}

	callSendAPI(sender_psid, message)

# ====== User functionality ===== #

# TODO: move these into functions module

def check_user_exists(sender_psid):

	sender = models.Sender.select().where(models.Sender.psid == sender_psid)

	# if user does not exist, create the user and set bot variables
	if not sender.exists():
		data = humanisePSID(sender_psid)

		print("I SHOULD CREATE A MODEL:\npsid: {}\nfirst: {}\nlast: {}\nprofile: {}".format(sender_psid, data['first_name'], data['last_name'], data['profile_pic']))

		models.Sender.create(
			psid = sender_psid,
			first_name = data['first_name'],
			last_name = data['last_name'],
			profile_url = data['profile_pic'],
			last_message = datetime.datetime.now()
		)

		bot.set_uservars(str(sender_psid), {"first_name": data['first_name'], "last_name": data['first_name']})

	else:
		# just to make sure the server doesn't restart and shit up the vars
		sender = sender.get()
		bot.set_uservars(str(sender_psid), {"first_name": sender.first_name, "last_name": sender.last_name})
		sender.last_message = datetime.datetime.now()
		sender.save()

def humanisePSID(PSID):
	# url = "https://graph.facebook.com/" + str(PSID)

	# r = requests.get(
	# 	url,
	# 	params = {
	# 		"fields" : "first_name,last_name,profile_pic",
	# 		"access_token" : PAGE_ACCESS_TOKEN
	# 	}
	# )

	# if r.status_code == 200:
	# 	data = r.json()
	# 	print("Worked!")
	# 	return data
	# else:
	# 	print("FUCKED! PSID was: {}".format(str(PSID)))

	# I believe there is an issue using the live PAGE_ACCESS_TOKEN
	return {"first_name":"Meatbag","last_name":"Issue","profile_pic":"https:\/\/platform-lookaside.fbsbx.com\/platform\/profilepic\/?psid=1821155224639424&width=1024&ext=1553834016&hash=AeQZgIdp0EFa4cSG"}
