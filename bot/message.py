# Message.py
#
# Functionality that involves connecting and sending messages to
# the facebook Send API

import json
import requests
import datetime
from pprint import pprint

from rivescript import RiveScript

from bot.settings import *

from bot.Response import (
    Response,
    Button,
    URLButton,
    PostbackButton,
    CallButton,
    Message_Tag,
)
import bot.functions as functions
import bot.models as models

# ==== rivescript bot setup ==== #

bot = RiveScript()
bot.load_directory("./bot/brain")
bot.sort_replies()

# ==== rivescript subroutines ==== #

# These functions can be used in the rivescript documents
bot.set_subroutine("set_jd", functions.set_jd)
bot.set_subroutine("get_jd", functions.get_jd)
bot.set_subroutine("set_shop", functions.set_shop)
bot.set_subroutine("get_shop", functions.get_shop)

# ==== message handling ==== #


def handleMessage(sender_psid, received_message):
    """
	Handles a plain message request and determines what to do with it
	By word matching the content and sender_psid
	"""

    response = Response(sender_psid)
    received_message = received_message.lower()

    if (
        "dinner" in received_message
        or "lunch" in received_message
        or "breakfast" in received_message
    ):
        meal = functions.findMeal(received_message)
        addTime = functions.findTime(received_message)

        if not meal:
            response.text = (
                f"Someone hasn't updated the menu 🤦‍♀️... yell at {OFFICERS}"
            )

            # Send Message To Bot Officers
            for psid in OFFICER_PSIDS:
                Response(
                    psid,
                    text="The menu has not been updated. The people are crying.",
                    msg_type=Message_Tag.COMMUNITY_ALERT,
                ).send()

        response.text = functions.dinoRequest(meal, addTime)
        response.add_reply("What's dino like?")
        response.add_reply("Dinovote")

    elif (
        "dinopoll" in received_message
        or "dino like" in received_message
        or "dino good" in received_message
    ):

        response.text = functions.dinoPoll()
        response.add_reply("Dinovote")

    elif (
        "what's on" in received_message
        or "what’s on" in received_message
        or "what is on" in received_message
        or "event" in received_message
        or "calendar" in received_message
    ):
        eventAsset = functions.getWeekEvents()
        if eventAsset:
            response.asset = eventAsset
        else:
            response.text = "I can't find this week's calendar! Soz."

            for psid in OFFICER_PSIDS:
                Response(
                    psid,
                    text="I couldn't send the weekly calendar! Please update me!!",
                    msg_type=Message_Tag.COMMUNITY_ALERT,
                ).send()

    elif "nudes" in received_message or "noods" in received_message:
        response.asset = "270145943837548"
        # asset ID came from making cURL request to fb api
        # NOTE: you need to use the production Page Access Token to generate the asset for the nudes
        # i.e. ... won't work in DEV

    elif (
        "dino is shit" in received_message
        or "dino is bad" in received_message
        or "dino is good" in received_message
        or "dinovote" in received_message
        or "vote" in received_message
    ):
        response.text = "What was dino like this time?"
        response.add_button(PostbackButton("Dino was great! 😋", "goodvote"))
        response.add_button(PostbackButton("Dino was awful! 🤢", "badvote"))

    elif (
        "what's dino" in received_message
        or "what’s dino" in received_message
        or "what is dino" in received_message
        or "what's for dino" in received_message
        or "for dino" in received_message
        or "whats dino" in received_message
        or "dino" in received_message
    ):
        meal = functions.getCurrentDino()
        if not meal:
            response.text = (
                f"Someone hasn't updated the menu 🤦‍♀️... yell at {OFFICERS}"
            )

            # Send Message To Bot Officers
            for psid in OFFICER_PSIDS:
                Response(
                    psid,
                    text="The menu has not been updated. The people are crying.",
                    msg_type=Message_Tag.COMMUNITY_ALERT,
                ).send()
        else:
            addTime = functions.findTime(received_message)

            response.text = functions.dinoRequest(meal.type, addTime)
            response.add_reply("What's dino like?")
            response.add_reply("Dinovote")

    elif "days left" in received_message or "semester" in received_message:
        response.text = functions.semesterResponse()

    elif "room is" in received_message:
        name = functions.extractName(received_message)

        response.text = functions.getRoomNumber(name)

    else:
        reply = bot.reply(str(sender_psid), received_message)
        response.text = str(reply)

    if sender_psid == "cmd":
        return response.payload
    else:
        print("sent back:")
        pprint(response.payload)
        response.send()

        return "OK"


def handlePostback(sender_psid, received_postback):
    """
	Handles a postback request to the webhook and determines what
	functionality / response to call
	"""
    payload = received_postback["payload"]

    print("RECEIVED POSTBACK: ", received_postback)
    response = Response(sender_psid)

    if payload == "goodvote":
        response.text = "Sounds like a nice meal!"
        functions.makeDinoVote("goodvote")

    elif payload == "badvote":
        response.text = "Too bad it was gross :("
        functions.makeDinoVote("badvote")

    else:
        response.text = "[DEBUG] Received postback for some reason..."

    response.send()
    return "OK"


def sendBubbles(sender_psid):
    """
	Sends bubbles to sender
	TODO: Include timing so bubbles don't hang around for ages
	"""

    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": PAGE_ACCESS_TOKEN},
        json={"recipient": {"id": sender_psid}, "sender_action": "typing_on"},
    )

    if r.status_code == 200:
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

    message = {"attachment": {"type": type, "payload": {"attachment_id": str(assetID)}}}

    callSendAPI(sender_psid, message)


# ====== User functionality ===== #

# TODO: move these into functions module


def check_user_exists(sender_psid):

    sender = models.Sender.select().where(models.Sender.psid == sender_psid)

    # if user does not exist, create the user and set bot variables
    if not sender.exists():
        data = humanisePSID(sender_psid)

        print(
            "I SHOULD CREATE A MODEL:\npsid: {}\nfirst: {}\nlast: {}\nprofile: {}".format(
                sender_psid, data["first_name"], data["last_name"], data["profile_pic"]
            )
        )

        models.Sender.create(
            psid=sender_psid,
            first_name=data["first_name"],
            last_name=data["last_name"],
            profile_url=data["profile_pic"],
            last_message=datetime.datetime.now(),
        )

        bot.set_uservars(
            str(sender_psid),
            {"first_name": data["first_name"], "last_name": data["first_name"]},
        )

    else:
        # just to make sure the server doesn't restart and shit up the vars
        sender = sender.get()
        bot.set_uservars(
            str(sender_psid),
            {"first_name": sender.first_name, "last_name": sender.last_name},
        )
        sender.last_message = datetime.datetime.now()
        sender.save()


def humanisePSID(PSID):
    url = "https://graph.facebook.com/" + str(PSID)

    r = requests.get(
        url,
        params={
            "fields": "first_name,last_name,profile_pic",
            "access_token": PAGE_ACCESS_TOKEN,
        },
    )

    if r.status_code == 200:
        data = r.json()
        print("Worked!")
        return data
    else:
        print("FUCKED! PSID was: {}".format(str(PSID)))


# ==== Reset Bot ==== #
def resetBot():
    # Ensure that we are not doing J&D
    bot.set_variable("jd", None)  # setting to none == delete the variable from bot
    bot.set_variable("jd_loc", None)
    bot.set_variable("shop", None)
