# Message.py
#
# Functionality that involves connecting and sending messages to
# the facebook Send API
import traceback
from celery import Celery

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

celery = Celery('bot', broker=BROKER_URL)

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
def groupMessage(psids, text):
    print("GROUP MESSAGE", "'" + text + "'")
    for psid in psids:
        print("    psid:", psid)
        try:
            Response(psid, text=text).send(timeout=0.01)
        except requests.exceptions.ReadTimeout:
            pass

@celery.task(bind=True)
def celeryTest(self):
    import time
    print(BROKER_URL)
    print("start celery")
    time.sleep(5)
    print("end celery")
    return "hi"

# @celery.task(bind=True)
def massMessage(text):
    import time
    time.sleep(5)
    senders = models.Sender.select()
    psids = [x.psid for x in senders]
    groupMessage(psids, text)

def handleMessage(sender_psid, received_message):
    """
	Handles a plain message request and determines what to do with it
	By word matching the content and sender_psid
	"""

    response = Response(sender_psid)
    received_message = received_message.lower()
    if "psid" in received_message:
        Response(sender_psid, text=str(sender_psid)).send()
    elif (
        "dinner" in received_message
        or "lunch" in received_message
        or "breakfast" in received_message
        or 'dino' in received_message) and 'time' not in received_message:
        url = 'https://l.facebook.com/l.php?u=https%3A%2F%2Flookaside.fbsbx.com%2Ffile%2Fmenu%252015%2520-21%2520feb%25202021.pdf%3Ftoken%3DAWy5rD_kYfFf0Y9KNUaPmQaQjMqlWh4YfkU5AzbqN3vhFNJu9RHAqJr6UtEPUDHu8ocarTdDtMnXfLM0NdvKawACjVBnsLma1wCYbLlgOiLaTjo3VXsGy06UDBoO70S4MjixlzVrUf5VopgVbsOjWYIxcbRpoh5fV24rysT-L_J3Fn4TFEgn760VVfzacZzjN_94Jbamy3ZRmq9w4cNreu3-FqKb89dbLH0NxaEgJkGY5xlybtIeuAyyqi2euEQU8jDDK3SI7wxIDj74j4GqH0LsJfsRC9k6CgJfSJrj_F-IWEnhxufvwivUj0SSCNLWjyAMqbHuPl6TOyIV4D7fGq1dReTzJcwtTs5gfoqRABzK0kQHSrMpq8wDPL6NX41HaIKr0jCxERto3jUvqAjiXWLtwka7MIgouRkOxHzU0_WJB2X7JXyX6fY0fPSRR2NtKUhjLjbQlVx32aVxHuhvT90Ae_jFlkaGZ63Ltlz8pxRZx5CRRn9Qf2Bs7_FnucaLbBMWfhzwZqarmjaf4cjU6yzvZWZbBwppH95pX6_xk9LzdcoB9SftrzzIUp9_lrdtRgC_93L7MtO871AkQE6GsvHvCU7-qSpgAdo14mWQHjhIuyXVUrChC0vm12GvAZsgWeQKzM2-_JPPvmT3fuveVWR6X1j-6ZiQ8gnsjRIe2o_NAWDdJ7TE_yYUWYkMbRe3Y-Zh8r1nKYi-dC3A-naAVWuinqCwXt2OPZOocPNNYkiynJmuxH6fuEsFZ6gxvQ1HJv8&h=AT0JMF2N8uFFWbrW1FI-dM22z16Qzixujho-fypO9CIBB3J93fuTO74sTtyWx9-ItoN6cjrX-QdURxTgBi-pb8imH3TI5zsYKW_UWzXC_IZ66Xv111R8nFQqMBN-KJBFPctnFYFNIFdrUIyS5YTUXvrFqKFAIiajOGfUtw&__tn__=H-R&c[0]=AT06F55jl8ZifYwSuBvXub0cwirWDhhsOyr2bqXWyWOmNAdt7BAZn8dFsgWJBxwKlfJhS3XcKrvUVyB3kP4eRyC8VZw__SFJjZh6X5zx_cnMPzfRPr8O7HkyD8BE8uIgIlbHZTFyVihzSdfk6P6X53TcKcnqaAb5PUCiebLY6TUAHP6Eq0tH6Z8Avw044DO_gBzALhEqUPGAYhmPYNH_SG_O4_jSBg'
        Response(sender_psid, text=url).send()

    elif (
        "dinner" in received_message
        or "lunch" in received_message
        or "breakfast" in received_message
    ) and 'late meal' not in received_message:
        meal = functions.findMeal(received_message)
        addTime = functions.findTime(received_message)

        theMeal = functions.dinoRequestObj(meal, addTime)

        if not theMeal:
            response.text = (
                f"Someone hasn't updated the menu 🤦‍♀️... yell at {OFFICERS}"
            )
            text="The menu has not been updated. The people are crying."
            groupMessage(OFFICER_PSIDS, text)
            # Send Message To Bot Officers

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
            Response(sender_psid, image=eventAsset).send()
            response.text = "Here is this week's calendar!"
        else:
            response.text = "I can't find this week's calendar! Soz."

            text="I couldn't send the weekly calendar! Please update me!!"
            groupMessage(OFFICER_PSIDS, text)

    elif "nudes" in received_message or "noods" in received_message:
        # response.asset = "270145943837548"
        url = 'https://indomie.com.au/wp-content/uploads/2020/03/migorengjumbo-new.png'
        Response(sender_psid, image=url).send()

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
    ) and 'time' not in received_message:
        meal = functions.getCurrentDino()

        if not meal or meal is None:
            response.text = (
                f"Someone hasn't updated the menu 🤦‍♀️... yell at {OFFICERS}"
            )
            text="The menu has not been updated. The people are crying."
            groupMessage(OFFICER_PSIDS, text)
            # Send Message To Bot Officers

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
                r = Response(sender_psid, image=image.url)
                print('sending image')
                pprint(r.payload)
                r.send()
                Response(sender_psid, f"Photo by: {image.sender.full_name}").send()

    # Testing adding a new feature
    elif "snazzy pic" in received_message:
        meal = functions.getCurrentDino()
        if meal is not None and meal.images:
            image = random.choice([image for image in meal.images])
            Response(sender_psid, image=image.url).send()
            Response(sender_psid, f"Photo by: {image.sender.full_name}").send()
        else:
            Response(sender_psid, "No snazzy pics :(").send()

    elif "days left" in received_message or "semester" in received_message:
        response.text = functions.semesterResponse()

    elif 'am i a ressiexd' in received_message:
        pass
        '''
        ressie = models.Ressie.select().where(models.Ressie.facebook_psid == sender_psid).get()
        if ressie:
            response.text = f'Yes, we have you down as being {ressie.first_name} {ressie.last_name} in room {ressie.room_number}'
        else:
            response.text = 'Nah, we don\'t have you down as being a ressie here. Soz'
        '''

    elif 'order me a late meal' in received_message:
        try:
            meal, date = functions.orderLateMeal(received_message, sender_psid)
            response.text = f'Late meal ordered for {meal} on {date}!'
        except Exception as e:
            response.text = 'Uh oh! Something went wrong: ' + str(e)

    elif "room is" in received_message:
        try:
            ressie = getRessieBySender(sender_psid)
        except:
            response.text = 'Sorry, we don\'t have you down as a resident of Baxter. If you think there\'s a mistake then contact Nick!'
        name = functions.extractName(received_message)
        print("trying find room for", name)
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
            Response(sender_psid, "You can't have more than 5 crushes!").send()
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
    print("check_user_exists")
    sender = models.Sender.select().where(models.Sender.psid == sender_psid)
    data = functions.humanisePSID(sender_psid)

    if not data:
        print("received message from ghost!")
        return

    # Link them to the Ressie table if they are a Ressie
    name = data['first_name'] + ' ' + data['last_name']
    try:
        _, confidence, ressie = models.Ressie.fuzzySearch(name)
        if confidence <= 70:
            raise Exception

        '''
        if not ressie.facebook_psid:
            ressie.facebook_psid = sender_psid
            ressie.save()
        '''
    except Exception as e:
        print(Exception, e)
        traceback.print_exc()
        pass
        # The FB user probably isn't from Baxter

    print(sender)
    # if user does not exist, create the user and set bot variables
    with models.db.atomic() as trans:
        trans.rollback()
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



# ==== Reset Bot ==== #
def resetBot():
    # Ensure that we are not doing J&D
    bot.set_variable("jd", None)  # setting to none == delete the variable from bot
    bot.set_variable("jd_loc", None)
    bot.set_variable("shop", None)
