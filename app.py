# app.py
#
# Runs and handles all connections to the web server
# trying to fix probs

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    send_from_directory,
)
import os
import json
import requests
import datetime
import mammoth
import re
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup

import argparse

from bot.settings import *

from bot.Response import Response
import bot.models as models
import bot.message as message
import bot.functions as functions

if DEBUG:
    print(
        "\n\n\nTHIS IS A LOCAL VERSION\n-> Ensure you set ngrok webhook URL in fb\n-> Ensure PAGE_ACCESS_TOKEN is set\n-> Make sure POSTGRES is Running!!!\n\n"
    )

# import logging
# import http.client as http_client

# http_client.HTTPConnection.debuglevel = 1

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":

        response = {"text": request.form["message"]}

        for user in models.Sender.select():
            message.callSendAPI(user.psid, response)

        return render_template("update.html")
    else:
        return render_template("update.html")


@app.route("/webhook", methods=["POST", "GET"])
def webhook():

    if request.method == "POST":
        print("SOMEONE SENT MESSAGE!")
        body = request.json
        print(body)

        if body["object"] == "page":  # check it is from a page subscription

            # there may be multiple entries if it is batched
            for entry in body["entry"]:

                # get the message
                webhook_event = entry["messaging"][0]

                # get the sender PSID
                sender_psid = None
                sender_psid = webhook_event["sender"]["id"]

                sender = message.check_user_exists(sender_psid)

                if sender.conversation and "message" in webhook_event:
                    return message.handleConversation(
                        sender_psid, webhook_event["message"], sender.conversation
                    )

                if "postback" in webhook_event:
                    # handle the postback
                    return message.handlePostback(
                        sender_psid,
                        webhook_event["postback"],
                        webhook_event["message"]["text"],
                    )
                elif "message" in webhook_event:
                    # handle the message
                    if (
                        "quick_reply" in webhook_event["message"]
                        and "payload" in webhook_event["message"]["quick_reply"]
                    ):
                        print("Got payload!")
                        return message.handlePostback(
                            sender_psid,
                            webhook_event["message"]["quick_reply"],
                            webhook_event["message"]["text"],
                        )
                    elif "text" in webhook_event["message"]:
                        return message.handleMessage(
                            sender_psid, webhook_event["message"]["text"]
                        )
                    else:
                        return Response(
                            sender_psid,
                            text=f"I can't deal with whatever shit you just sent me. Go complain to {OFFICERS} about it",
                        ).send()
                else:
                    return Response(
                        sender_psid,
                        text=f"I can't deal with whatever shit you just sent me. Go complain to {OFFICERS} about it",
                    ).send()

        else:
            # send error
            print("Something went shit")
            return "Not Okay"

    elif request.method == "GET":
        print("SOMEONE IS REQUESTING TOKEN")
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode and token:  # the mode and token are in the query string

            if mode == "subscribe" and token == VERIFY_TOKEN:

                # respond with the challenge token from the request
                print("WEBHOOK VERIFIED")
                return challenge

            else:
                print("403 WEBHOOK NOT VERIFIED")
                return "403"
                # send 403 error

    else:
        print("Someone decided to be an idiot.")


# ====== Upload Asset ====== #


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        # do image upload
        url = request.form["assetURL"]
        response = functions.uploadAsset(url)

        models.WeekCal.create(
            assetID=response["attachment_id"], week_start=request.form["date"]
        )

    assets = models.WeekCal.select()

    return render_template("upload.html", assets=assets)


# ====== Add a meal ====== #


@app.route("/dino")
def dino():
    meals = models.Meal.select().order_by(models.Meal.date.desc())
    return render_template("dino.html", meals=meals)


@app.route("/dino/add", methods=["POST"])
def addMeal():
    form = request.form
    models.Meal.create(
        date=form["date"], description=form["description"], type=form["type"]
    )
    return redirect(url_for("dino"))


@app.route("/dino/batch/add", methods=["POST"])
def batchAddMeal():
    form = request.form
    for meal in ["breakfast", "lunch", "dinner"]:
        models.Meal.create(
            date=form["date"], description=form[meal + "_description"], type=meal
        )
    return redirect(url_for("dino"))


@app.route("/dino/delete/<int:meal_id>", methods=["GET"])
def deleteMeal(meal_id):
    meal = models.Meal.select().where(models.Meal.id == meal_id).get()
    meal.delete_instance()
    return redirect(url_for("dino"))

@app.route("/dino/batchdelete", methods=["POST"])
def deleteBatchMeals():
    form = request.form
    for strId in form.getlist("delete"):
        mealId = int(strId)
        meal = models.Meal.select().where(models.Meal.id == mealId).get()
        meal.delete_instance()
    return redirect(url_for("dino"))


@app.route("/dino/fileadd", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            print("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            print("No selected file")
            return redirect(request.url)
        if file.filename.endswith(".docx"):
            result = mammoth.convert_to_html(file)
            html = result.value  # The generated HTML
            messages = (
                result.messages
            )  # Any messages, such as warnings during conversion

            extracted = functions.dinoparse(html)
            return render_template("checkParser.html", extracted=extracted)
        if file.filename.endswith(".html") or file.filename.endswith(".htm"):
            mealsByDay = functions.dinoparse(file.readlines())
            return render_template("checkParser.html", mealsByDay=mealsByDay)
    else:
        return redirect(url_for("dino"))


@app.route("/dino/file/confirm", methods=["POST"])
def confirm_file():
    form = request.form
    meals = ["breakfast", "lunch", "dinner"]
    for day in range(1, 8):
        date = form[str(day) + "/" + "date"]
        for meal in range(1, 4):
            things = form.getlist(str(day) + "/" + str(meal))
            description = "\n\n".join(things)

            subs = {"&amp;": "&", "\\x96": "-", "\\x92": "'", "\\u2019":"'", "\\u2018":"'", "\\u2013": "-"}

            for sub, repl in subs.items():
                description = re.sub(sub, repl, description)
            print("\n\n here we go:", date, "\n\ndescr: ", description, "\n\nmeal", meals[meal - 1])
            models.Meal.create(date=date, description=description, type=meals[meal - 1])
    return redirect(url_for("dino"))


# ======= Resident Information ======= #
@app.route("/ressie", methods=["POST", "GET"])
def resident():

    if request.method == "POST":
        # do resident creation

        models.Ressie.create(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            room_number=request.form["room_number"],
            floor=int(
                str(request.form["room_number"])[:1]
            ),  # get the first digit of the room number and set that as floor
        )

    ressies = models.Ressie.select()

    return render_template("ressie.html", ressies=ressies)


@app.route("/ressie/delete/<int:ressie_id>", methods=["GET"])
def deleteRessie(ressie_id):
    ressie = models.Ressie.select().where(models.Ressie.id == ressie_id).get()
    ressie.delete_instance()
    return redirect(url_for("resident"))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--terminal", help="Run Baxtabot in the terminal", action="store_true"
    )
    args = parser.parse_args()

    models.goGoPowerRangers()
    message.resetBot()

    if args.terminal:
        while True:
            msg = str(input("> "))
            print("BAXTABOT: ", message.handleMessage("cmd", msg)["message"]["text"])
    else:
        app.run(debug=DEBUG, port=PORT, host="0.0.0.0")

