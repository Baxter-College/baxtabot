from flask import Flask, request, render_template, redirect, url_for
import os
import json
import requests
import datetime

from environment import *

import models
import message

# TO add a test user - go to: https://developers.facebook.com/requests/

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

@app.route('/privacy')
def privacy():
	return render_template('privacy.html')

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
					return message.handleMessage(sender_psid, webhook_event['message']['text'])
				elif (webhook_event['message']['quick_reply']):
					return message.handlePostback(sender_psid, webhook_event['message']['quick_reply']['payload'])
				elif (webhook_event['postback']):
					return message.handlePostback(sender_psid, webhook_event['postback'])

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
