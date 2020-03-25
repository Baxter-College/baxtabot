# Message.py
#
# Functionality that involves connecting and sending messages to
# the facebook Send API

import random
import json
import requests
import datetime
from bot.sonnets import sonnetGen
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
    Reply,
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
bot.set_subroutine("set_hashbrowns", functions.set_hashbrowns)
bot.set_subroutine("get_hashbrowns", functions.get_hashbrowns)

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

        theMeal = functions.dinoRequestObj(meal, addTime)

        if not theMeal:
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
            response.text = (
                functions.dinoRequest(meal, addTime)
                # + f"\n\n💕==========💕\nThis dino update brought to you by my undying and eternal love for Jacinta Wright.\n Here is a generated love sonnet:\n {sonnetGen()}"
            )
            response.add_reply(Reply("Add Image", payload="DINOIMAGE"))
            response.add_reply(Reply("Whats dino like?"))
            response.add_reply(Reply("Dinovote"))

            if theMeal.images:
                image = random.choice([image for image in theMeal.images])
                Response(sender_psid, image=image.url).send()
                Response(sender_psid, f"Photo by: {image.sender.full_name}").send()

    elif (
        "dinopoll" in received_message
        or "dino like" in received_message
        or "dino good" in received_message
    ):

        response.text = functions.dinoPoll()
        response.add_reply(Reply("Dinovote"))

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

            response.text = (
                functions.dinoRequest(meal.type, addTime)
                # + f"\n\n💕==========💕\nThis dino update brought to you by my unending and eternal love for Jacinta Wright. Here is a generated love sonnet:\n {sonnetGen()}"
            )
            response.add_reply(Reply("What's dino like?"))
            response.add_reply(Reply("Dinovote"))
            response.add_reply(Reply("Add Image", payload="DINOIMAGE"))

            if meal.images:
                image = random.choice([image for image in meal.images])
                Response(sender_psid, image=image.url).send()
                Response(sender_psid, f"Photo by: {image.sender.full_name}").send()

    elif "days left" in received_message or "semester" in received_message:
        response.text = functions.semesterResponse()

    elif 'am i a ressie' in received_message:
        ressie = models.Ressie.select().where(models.Ressie.facebook_psid == sender_psid).get()
        if ressie:
            response.text = f'Yes, we have you down as being {ressie.first_name} {ressie.last_name} in room {ressie.room_number}'
        else:
            response.text = 'Nah, we don\'t have you down as being a ressie here. Soz'

    elif "room is" in received_message:
        name = functions.extractName(received_message)

        response.text = functions.getRoomNumber(name)

    elif "crush list" in received_message:
        me = models.Sender.select().where(models.Sender.psid == sender_psid).get()

        if not len(me.crushes):
            response.text = "You have no crushes"
        else:
            crushList = "Your crush list:\n"
            for crush in me.crushes:
                crushList += crush.crushee.full_name + "\n"
            response.text = crushList
            response.add_reply(Reply("Remove Crush", payload="REMOVECRUSH"))

        response.add_reply(Reply("Add Crush", payload="ADDCRUSH"))

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


def handlePostback(sender_psid, received_postback, msg):
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

    elif payload == "ADDCRUSH":
        start_conversation(sender_psid, "ADDCRUSH")
        response.text = "Enter your crush name:"

    elif payload == "REMOVECRUSH":
        start_conversation(sender_psid, "REMOVECRUSH")
        response.text = "Enter the crush name to remove:"

    elif payload == "DINOIMAGE":
        start_conversation(sender_psid, "DINOIMAGE")
        response.text = "Send me a photo of dino!"

    else:
        # response.text = "[DEBUG] Received postback for some reason..."
        handleMessage(sender_psid, msg)
        return "OK"

    response.send()
    return "OK"


def handleConversation(sender_psid, received_msg, conversation):

    if "text" in received_msg:
        msg_text = received_msg["text"]

    me = models.Sender.select().where(models.Sender.psid == sender_psid).get()

    if conversation == "ADDCRUSH":
        # Check if we have more than 5 crushes already
        if len(me.crushes) >= 5:
            Response(semder_psid, "You can't have more than 5 crushes!").send()
            # End the conversation
            me.conversation = None
            me.save()
            return "OK"

        _, confidence, myCrush = models.Sender.fuzzySearch(msg_text)

        me.add_crush(myCrush)

        r = Response(sender_psid, f"Added {myCrush.full_name} to crush list")
        r.add_reply(Reply("Add another Crush", payload="ADDCRUSH"))
        r.send()

        if int(sender_psid) in [crush.crushee.psid for crush in myCrush.crushes]:
            # You are the crush of your crush. It's a match!
            msg = f"Congrats! {myCrush.full_name} is crushing on you! Matchmaker Baxtabot is here to match! You now have a date at {random.choice(DATE_LOCATIONS)} at {random.choice(range(6))}pm tomorrow. Clear you calendar - this is your chance 😉😘😜"
            Response(sender_psid, msg).send()
            Response(myCrush.psid, msg).send()

    elif conversation == "REMOVECRUSH":
        _, confidence, myCrush = models.Sender.fuzzySearch(msg_text)

        for aCrush in me.crushes:
            if aCrush.crushee.psid == myCrush.psid:
                Response(
                    sender_psid, f"Removed {aCrush.crushee.full_name} from crush list"
                ).send()
                aCrush.delete_instance()

        Response(sender_psid, "Done!").send()

    elif conversation == "DINOIMAGE":
        if "attachments" in received_msg and received_msg["attachments"][0]:
            dino = functions.getCurrentDino()
            sender = (
                models.Sender.select().where(models.Sender.psid == sender_psid).get()
            )
            img = models.MealImg.create(
                meal=dino.id,
                url=received_msg["attachments"][0]["payload"]["url"],
                sender=sender.id,
            )
            Response(sender_psid, image=img.url).send()
            Response(sender_psid, "What a stunning shot!").send()
        else:
            Response(sender_psid, "You need to send me an image!").send()

    # End the conversation
    me.conversation = None
    me.save()
    return "OK"


def start_conversation(sender_psid, conversation):
    sender = models.Sender.select().where(models.Sender.psid == sender_psid).get()
    sender.conversation = conversation
    sender.save()


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
    data = humanisePSID(sender_psid)

    # Link them to the Ressie table if they are a Ressie
    name = data['first_name'] + ' ' + data['last_name']
    try:
        _, confidence, ressie = models.Ressie.fuzzySearch(name)
        if confidence <= 70:
            raise Exception
        if not ressie.facebook_psid:
            ressie.facebook_psid = sender_psid
            ressie.save()
    except:
        pass
        # The FB user probably isn't from Baxter

    # if user does not exist, create the user and set bot variables
    if not sender.exists():

        print(
            "I SHOULD CREATE A MODEL:\npsid: {}\nfirst: {}\nlast: {}\nprofile: {}".format(
                sender_psid, data["first_name"], data["last_name"], data["profile_pic"]
            )
        )

        sender = models.Sender.create(
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

        # update name incase they've changed...
        sender.first_name = data["first_name"]
        sender.last_name = data["last_name"]

        bot.set_uservars(
            str(sender_psid),
            {"first_name": sender.first_name, "last_name": sender.last_name},
        )
        sender.last_message = datetime.datetime.now()
        sender.save()

    # if the sender did not reply to the conversation within 1 mins, delete the conversation.
    if sender.conversation:
        if (datetime.datetime.now() - sender.last_message).seconds > 60:
            sender.conversation = None
            sender.save()

    return sender

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
