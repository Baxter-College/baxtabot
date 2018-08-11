from flask import Flask, request, render_template, redirect, url_for
import os
import json
import requests
import datetime

from rivescript import RiveScript

import models

# TO add a test user - go to: https://developers.facebook.com/requests/

bot = RiveScript()
bot.load_directory("./brain")
bot.sort_replies()

# vv for when it all goes to shit vv

# import logging
# import http.client as http_client
#
# http_client.HTTPConnection.debuglevel = 1
#
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

app = Flask(__name__)

DEBUG = int(os.environ.get('DEBUG'))
PORT = int(os.environ.get('PORT'))
# DEBUG = 1
# PORT = 8000

PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = "GoodLordyThomasJHillLooksFineTonight"

@app.before_request
def before_request():
	models.db.connect()

@app.after_request
def after_request(response):
	models.db.close()
	return response

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():

	if request.method == 'POST':
		print("SOMEONE SENT MESSAGE!")
		body = request.json
		print(body)

		if body['object'] == 'page': # check it is from a page subscription

			for entry in body['entry']: #there may be multiple entries if it is batched

				# get the message
				webhook_event = entry['messaging'][0]
				print(webhook_event)

				# get the sender PSID
				sender_psid = webhook_event['sender']['id']
				print("Sender ID: {}".format(sender_psid))

				if (webhook_event['message']['text']):
					return handleMessage(sender_psid, webhook_event['message']['text'])
				elif (webhook_event['message']['quick_reply']):
					return handlePostback(sender_psid, webhook_event['message']['quick_reply']['payload'])
				elif (webhook_event['postback']):
					return handlePostback(sender_psid, webhook_event['postback'])

		else:
			# send error
			print("Something went shit")
			return 'Not Okay'

	elif request.method == 'GET':
		print("SOMEONE IS REQUESTING TOKEN")
		mode = request.args.get('hub.mode')
		token = request.args.get('hub.verify_token')
		challenge = request.args.get('hub.challenge')

		if (mode and token): # the mode and token are in the query string

			if (mode == "subscribe" and token == VERIFY_TOKEN):

				# respond with the challenge token from the request
				print("WEBHOOK VERIFIED")
				return challenge

			else:
				print('403 WEBHOOK NOT VERIFIED')
				return '403'
				# send 403 error

	else:
		print("Someone decided to be an idiot.")

# ==== message handling ==== #

def handleMessage(sender_psid, received_message):
	print("HANDLING MESSAGE!")
	response = {}

	received_message = received_message.lower()

	if ("dinner" in received_message or "lunch" in received_message or "breakfast" in received_message):
		response = {"text": dinoRequest(received_message)}
	elif ("date" in received_message):
		response = {"text": "The date is: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))}
	elif ("dino is shit" in received_message or "dino is good" in received_message or "dinovote" in received_message):
		response = dinoVote()
	elif ("duty tutor" in received_message or "locked out" in received_message):
		response = {
			"attachment":{
				"type":"template",
				"payload":{
					"template_type":"button",
					"text":"Locked out again?! 🤦‍♂️",
					"buttons":[
						  {
						    "type":"phone_number",
						    "title":"Call the Duty Tutor",
						    "payload":"9385 9786"
						  }
					]
				}
			}
		}
	else:
		reply = bot.reply(str(sender_psid), received_message)
		response = {"text": "{}".format(reply)}

	print("Sending back: ")
	print(response)

	callSendAPI(sender_psid, response)

	return 'OK'

def handlePostback(sender_psid, received_postback):

	print('RECEIVED POSTBACK: ', received_postback)
	response = {"text": "Worked!"}

	callSendAPI(sender_psid, response)

def callSendAPI(sender_psid, response):

	r = requests.post(
		"https://graph.facebook.com/v2.6/me/messages",
		params = { "access_token": PAGE_ACCESS_TOKEN },
		json = {
			#"messaging_type": "RESPONSE", # alternatively MESSAGE_TAG
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
		print("It's all gone to shit!")
		return "It's all gone to shit", r.status_code

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

# ====== Add a meal ====== #

@app.route('/dino')
def dino():
	meals = models.Meal.select()
	return render_template('dino.html', meals=meals)

@app.route('/dino/add', methods=['POST'])
def addMeal():
	form = request.form
	models.Meal.create(
		date = form['date'],
		description = form["description"],
		type = form["type"]
	)
	return redirect(url_for('dino'))

@app.route('/dino/batch/add', methods=['POST'])
def batchAddMeal():
	form = request.form
	for meal in ["breakfast", "lunch", "dinner"]:
		models.Meal.create(
			date = form['date'],
			description = form[meal + "_description"],
			type = meal
		)
	return redirect(url_for('dino'))

@app.route('/dino/delete/<int:meal_id>', methods=['GET'])
def deleteMeal(meal_id):
	meal = models.Meal.select().where(models.Meal.id == meal_id).get()
	meal.delete_instance()
	return redirect(url_for('dino'))

if __name__ == '__main__':
	models.goGoPowerRangers()
	app.run(debug=DEBUG, port=PORT, host='0.0.0.0')
