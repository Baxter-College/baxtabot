from flask import Flask, request
import os
import json
import requests

app = Flask(__name__)

DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = "GoodLordyThomasJHillLooksFineTonight"

@app.before_request
def before_request():
	# connect to db
	pass

@app.after_request
def after_request(response):
	# close connection to db
	return response

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():

	if request.method == 'POST':
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

				if (webhook_event['message']):
					return handleMessage(sender_psid, webhook_event['message'])
				elif (webhook_event['postback']):
					return handlePostback(sender_psid, webhook_event['postback'])


		else:
			# send error
			pass

	elif request.method == 'GET':

		mode = request.args.get('hub.mode')
		token = request.args.get('hub.verify_token')
		challenge = request.args.get('hub.challenge')

		if (mode and token): # the mode and token are in the query string

			if (mode == "subscribe" and token == VERIFY_TOKEN):

				# respond with the challenge token from the request
				print("WEBHOOK VERIFIED")
				return challenge

			else:
				pass
				# send 403 error

	else:
		print("Someone decided to be an idiot.")

# ==== message handling ==== #

def handleMessage(sender_psid, received_message):

	response = {}

	if (received_message):
		response = {"text": "You sent: {}".format(received_message)}
		print("got to handle message")
	callSendAPI(sender_psid, response)

	return 'OK'

def handlePostback(sender_psid, received_postback):

	callSendAPI(sender_psid, response)

def callSendAPI(sender_psid, response):

	request_body = {
		"recipient": {
			"id": sender_psid
		},
		"message": response
	}

	r = requests.post(
		"https://graph.facebook.com/v2.6/me/messages",
		params = { "access_token": PAGE_ACCESS_TOKEN },
		data = {
			"json": json.dumps(request_body)
		}
	)

	print("sent message to meatbag!")

	return "OK"

if __name__ == '__main__':
	app.run(debug=DEBUG, port=PORT, host=HOST)