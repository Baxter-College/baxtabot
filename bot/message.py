'''
# Message.py
#
# Functionality that involves connecting and sending messages to
# the facebook Send API
'''
import traceback

import random
import time
import datetime
from pprint import pprint

import requests
from celery import Celery
from rivescript import RiveScript

# from bot.settings import *
from bot.settings import (
    BROKER_URL, OFFICERS, OFFICER_PSIDS,
    PAGE_ACCESS_TOKEN, DATE_LOCATIONS
)
# from bot.sonnets import sonnetGen
from bot.Response import (
    Response,
    # Button,
    URLButton,
    PostbackButton,
    # CallButton,
    # Message_Tag,
    Reply,
)
import bot.functions as functions
import bot.models as models


def set_jd(rs, switch):

    jd_desc = ""

    try:
        if switch[1]:
            bot.set_variable("jd_loc", switch[1])
            jd_desc = " in the {}".format(switch[1])
    except:
        bot.set_variable("jd_loc", None)

    if switch[0].lower() == "on":
        bot.set_variable("jd", True)
        # jd = True
        return "COFFEE TIME!!! ☕️\nJ&D is ON" + jd_desc
    else:
        bot.set_variable("jd", None)
        bot.set_variable("jd_loc", None)
        return "No more coff! 😭"


def get_jd(rs, args):

    jd = bot.get_variable("jd")
    jd_loc = bot.get_variable("jd_loc")

    jd_desc = ""

    if jd_loc:
        jd_desc = " in the {}".format(jd_loc)

    if jd:
        return "J&D is ON" + jd_desc
    else:
        return "J&D is OFF 😭 😭 😭"

def set_shop(rs, switch):

    if switch[0].lower() == "on":
        bot.set_variable("shop", True)
        return "Shopen!"
    else:
        bot.set_variable("shop", None)
        return "Shclosed 😭"


def get_shop(rs, args):

    shop = bot.get_variable("shop")

    return "Shopen!!!" if shop else "Shclosed 😭"

celery = Celery('bot', broker=BROKER_URL)

# ==== rivescript bot setup ==== #

bot = RiveScript()
bot.load_directory("./bot/brain")
bot.sort_replies()

# ==== rivescript subroutines ==== #

# These functions can be used in the rivescript documents
bot.set_subroutine("set_jd", set_jd)
bot.set_subroutine("get_jd", get_jd)
bot.set_subroutine("set_shop", set_shop)
bot.set_subroutine("get_shop", get_shop)
# bot.set_subroutine("set_hashbrowns", functions.set_hashbrowns)
# bot.set_subroutine("get_hashbrowns", functions.get_hashbrowns)

# ==== message handling ==== #
def groupMessage(psids, text):
    '''
    Sends a message to a group of people
    '''
    print("GROUP MESSAGE", "'" + text + "'")
    for psid in psids:
        print("    psid:", psid)
        try:
            Response(psid, text=text).send(timeout=0.01)
        except requests.exceptions.ReadTimeout:
            pass

@celery.task(bind=True)
def celeryTest(self): # pylint: disable=unused-argument
    ## What does this code do?? NP
    print(BROKER_URL)
    print("start celery")
    time.sleep(5)
    print("end celery")
    return "hi"

# @celery.task(bind=True)
def massMessage(text):
    time.sleep(5)
    senders = models.Sender.select()
    psids = [x.psid for x in senders]
    groupMessage(psids, text)

def is_dino_message(received_message):
    return ("dinner" in received_message
    or "lunch" in received_message
    or "breakfast" in received_message
    or "what's dino" in received_message
    or "what’s dino" in received_message
    or "what is dino" in received_message
    or "what's for dino" in received_message
    or "for dino" in received_message
    or "whats dino" in received_message
    or "dino" in received_message) and (
        'late meal' not in received_message
    ) and ('time' not in received_message)

def handle_dino_message(sender_psid, response, received_message):
    '''
    Handles a message related to dino.

    Return value: response message

    Side effects:
    - Sends an image of dino if exists
    '''
    meal = functions.findMeal(received_message)
    addTime = functions.findTime(received_message)

    if not meal:
        theMeal = functions.getCurrentDino()
    else:
        theMeal = functions.dinoRequestObj(meal, addTime)
    if not theMeal:
        text = (
            f"Someone hasn't updated the menu 🤦‍♀️... yell at {OFFICERS}"
        )
        message = "The menu has not been updated. The people are crying."
        groupMessage(OFFICER_PSIDS, message)
        # Send Message To Bot Officers

    else:
        text = (
            functions.dinoRequest(theMeal.type, addTime)
            # + f"\n\n💕==========💕\nThis dino update brought to you
            # by my undying and eternal love for Jacinta Wright.\n
            # Here is a generated love sonnet:\n {sonnetGen()}"
        )
        response.add_reply(Reply("Add Image", payload="DINOIMAGE"))
        response.add_reply(Reply("Whats dino like?"))
        response.add_reply(Reply("Dinovote"))
        response.add_button(URLButton('Dino Feedback Form!', 'https://forms.office.com/Pages/ResponsePage.aspx?id=pM_2PxXn20i44Qhnufn7o91DYUQ6lW9MsGLk8aV9AgNUNEJUWlVMOUNFUlRFNk1CSkFIQVJDMEFYTi4u&qrcode=true'))

        send_dinoimages(sender_psid, theMeal)

    return text

def handle_dinowrong_message(sender_psid, response):
    response.add_reply(Reply('Dino is wrong?', payload='DINOWRONG'))
    return 'Oh no! Is the dino menu wrong??'

# Sends own response
def handle_dinopoll_message(response):
    '''
    Responds to request to poll for dino

    Side effects:
    - Adds a reply option to the response
    '''
    response.add_reply(Reply("Dinovote"))
    return functions.dinoPoll()

# Sends own response + returns response
def handle_calendar_message(sender_psid):
    '''
    Sends the calendar

    Return value:
    - "Here is this week's calendar!" || "Here is this week's calendar!"

    Side effects:
    - Sends an image with the calendar
    '''
    eventAsset = functions.getWeekEvents()

    if eventAsset:
        Response(sender_psid, image=eventAsset).send()
        return "Here is this week's calendar!"
    text="I couldn't send the weekly calendar! Please update me!!"
    groupMessage(OFFICER_PSIDS, text)

    return "Here is this week's calendar!"


# Sends own response
def handle_dinovote_message(response):
    '''
    Creates a poll for dino

    Return value: "What was dino like this time?"

    Side effects:
    - Adds 2 buttons to the response
    '''
    response.add_button(PostbackButton("Dino was great! 😋", "goodvote"))
    response.add_button(PostbackButton("Dino was awful! 🤢", "badvote"))
    return "What was dino like this time?"

# Sends own response
def send_dinoimages(sender_psid, meal):
    if meal.images:
        # image = random.choice([image for image in meal.images])
        image = random.choice(list(meal.images))
        Response(sender_psid, image=image.url).send()
        Response(sender_psid, f"Photo by: {image.sender.full_name}").send()
    else:
        Response(sender_psid, "No snazzy pics :(").send()

# Returns text
def handle_latemeal_message(sender_psid, received_message):
    '''
    Orders a late dino

    Exceptions:
    - General error raising (FIX THIS LATER)
    '''
    try:
        meal, date = functions.orderLateMeal(received_message, sender_psid)
        return f'Late meal ordered for {meal} on {date}!'
    except Exception as excp: # pylint: disable=broad-except
        return 'Uh oh! Something went wrong: ' + str(excp)

# Returns text
def handle_getroom_message(sender_psid, received_message):
    '''
    Handles a message asking for a room

    Return value:
        If the sender is not a resident at Baxter, gives them a friendly message.
        Otherwise, finds the room of the resident specified in the message.
    '''

    try:
        functions.getRessieBySender(sender_psid)
    except Exception as excp: # pylint: disable=broad-except
        return (f'{excp} Sorry, we don\'t have you down as a resident of Baxter. ' +
        'If you think there\'s a mistake then contact Nick!')
    else:
        name = functions.extractName(received_message)
        print('name is', name)
        return functions.getRoomNumber(name)

# Sends own response
def handle_crushlist_message(sender_psid, response):
    '''
    Handles message to ask for crushlist

    Return value:
    - If they have no crushes "You have no crushes"
    - If they have crushes "Your crush list" + crush list

    Side effects:
    - Adds a reply to add + remove crushes to the response
    '''
    me = models.Sender.select().where(models.Sender.psid == sender_psid).get()

    if not len(me.crushes): # pylint: disable=len-as-condition
        text = "You have no crushes"
    else:
        crushList = "Your crush list:\n"
        for crush in me.crushes:
            crushList += crush.crushee.full_name + "\n"
        text = crushList
        response.add_reply(Reply("Remove Crush", payload="REMOVECRUSH"))

    response.add_reply(Reply("Add Crush", payload="ADDCRUSH"))
    return text

# pylint: disable=too-many-branches
def handleMessage(sender_psid, received_message):
    """
	Handles a plain message request and determines what to do with it
	By word matching the content and sender_psid
	"""

    received_message = received_message.lower()
    response = Response(sender_psid)
    print(sender_psid)

    if "psid" in received_message:
        Response(sender_psid, text=str(sender_psid)).send()
    elif (
        "dinopoll" in received_message
        or "dino like" in received_message
        or "dino good" in received_message
    ):
        response.text = handle_dinopoll_message(response)
    elif (
        "what's on" in received_message
        or "what’s on" in received_message
        or "what is on" in received_message
        or "event" in received_message
        or "calendar" in received_message
    ):
        response.text = handle_calendar_message(sender_psid)

    elif 'dino is wrong' in received_message:
        response.text = handle_dinowrong_message(sender_psid, response)

    elif "nudes" in received_message or "noods" in received_message:
        # response.asset = "270145943837548"
        url = 'https://indomie.com.au/wp-content/uploads/2020/03/migorengjumbo-new.png'
        Response(sender_psid, image=url).send()
    elif (
        "dino is shit" in received_message
        or "dino is bad" in received_message
        or "dino is good" in received_message
        or "dinovote" in received_message
        or "vote" in received_message
    ):
        response.text = handle_dinovote_message(response)
    elif is_dino_message(received_message):
        response.text = handle_dino_message(sender_psid, response, received_message)
        # Response(sender_psid, text='Arc Board elections are currently underway. If you want someone to vote for, Nick Patrikeos who helps maintain me is running. Type "arc board" for more info!').send()
    elif "snazzy pic" in received_message:

        meal = functions.getCurrentDino()
        if meal is not None and meal.images:
            image = random.choice(list(meal.images))
            Response(sender_psid, image=image.url).send()
            Response(sender_psid, f"Photo by: {image.sender.full_name}").send()
        else:
            Response(sender_psid, "No snazzy pics :(").send()

    elif 'am i a ressiexd' in received_message:
        pass

    elif 'order me a late meal' in received_message:
        response.text = handle_latemeal_message(sender_psid, received_message)

    elif "room is" in received_message:
        response.text = handle_getroom_message(sender_psid, received_message)

    elif "crush list" in received_message:
        response.text = handle_crushlist_message(sender_psid, response)

    else:
        reply = bot.reply(str(sender_psid), received_message)
        response.text = str(reply)

    if sender_psid == "cmd":
        return response.payload

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

    elif payload == 'DINOWRONG':
        start_conversation(sender_psid, 'DINOWRONG')
        response.text = 'What is the dino meal actually?'

    else:
        # response.text = "[DEBUG] Received postback for some reason..."
        handleMessage(sender_psid, msg)
        return "OK"

    response.send()
    return "OK"

def handle_dinowrong(sender_psid, received_message, me):
    print('The dino menu is wrong, should be', received_message)
    meal = functions.getCurrentDino()
    meal.description = received_message['text']
    meal.save()

    response = Response(sender_psid)
    response.text = handle_dino_message(sender_psid, response, 'dino')
    response.send()

    return 'Fixed!'


def handle_addcrush(sender_psid, received_message, me):
    # Check if we have more than 5 crushes already
    if len(me.crushes) >= 5:
        Response(sender_psid, "You can't have more than 5 crushes!").send()
        # End the conversation
        me.conversation = None
        me.save()
        return "OK"

    msg_text = received_message['text']
    _, confidence, myCrush = models.Sender.fuzzySearch(msg_text) # pylint: disable=unused-variable

    me.add_crush(myCrush)

    r = Response(sender_psid, f"Added {myCrush.full_name} to crush list")
    r.add_reply(Reply("Add another Crush", payload="ADDCRUSH"))
    r.send()

    if int(sender_psid) in [crush.crushee.psid for crush in myCrush.crushes]:
        # You are the crush of your crush. It's a match!
        msg = (f"Congrats! {myCrush.full_name} is crushing on you!" +
                " Matchmaker Baxtabot is here to match! You now have a date at" +
                f" {random.choice(DATE_LOCATIONS)} at {random.choice(range(1, 6))}pm tomorrow." +
                " Clear you calendar - this is your chance 😉😘😜")
        Response(sender_psid, msg).send()
        Response(myCrush.psid, msg).send()
    return 'OK'

def handle_removecrush(sender_psid, received_message, me):
    msg_text = received_message['text']
    _, confidence, myCrush = models.Sender.fuzzySearch(msg_text) # pylint: disable=unused-variable

    for aCrush in me.crushes:
        if aCrush.crushee.psid == myCrush.psid:
            Response(
                sender_psid, f"Removed {aCrush.crushee.full_name} from crush list"
            ).send()
            aCrush.delete_instance()

    Response(sender_psid, "Done!").send()

def handle_dinoimage(sender_psid, received_message):
    if "attachments" in received_message and received_message["attachments"][0]:
        dino = functions.getCurrentDino()
        sender = (
            models.Sender.select().where(models.Sender.psid == sender_psid).get()
        )
        img = models.MealImg.create(
            meal=dino.id,
            url=received_message["attachments"][0]["payload"]["url"],
            sender=sender.id,
        )
        Response(sender_psid, image=img.url).send()
        Response(sender_psid, "What a stunning shot!").send()
    else:
        Response(sender_psid, "You need to send me an image!").send()


def handleConversation(sender_psid, received_msg, conversation):

    # if "text" in received_msg:
    #    msg_text = received_msg["text"]

    me = models.Sender.select().where(models.Sender.psid == sender_psid).get()

    if conversation == "ADDCRUSH":
        handle_addcrush(sender_psid, received_msg, me)

    elif conversation == "REMOVECRUSH":
        handle_removecrush(sender_psid, received_msg, me)

    elif conversation == "DINOIMAGE":
        handle_dinoimage(sender_psid, received_msg)

    elif conversation == 'DINOWRONG':
        handle_dinowrong(sender_psid, received_msg, me)

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

    print("It's all gone to shit! -> ", r.status_code)
    return "It's all gone to shit", r.status_code

# pylint: disable=pointless-string-statement
'''
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
'''

# ====== User functionality ===== #

# TODO: move these into functions module
def check_user_exists(sender_psid):
    print("check_user_exists")
    sender = models.Sender.select().where(models.Sender.psid == sender_psid)
    data = functions.humanisePSID(sender_psid)

    if not data:
        print("received message from ghost!")
        return None

    # Link them to the Ressie table if they are a Ressie
    name = data['first_name'] + ' ' + data['last_name']
    try:
        _, confidence, ressie = models.Ressie.fuzzySearch(name) # pylint: disable=unused-variable
        if confidence <= 70:
            raise Exception

        # pylint: disable=pointless-string-statement
        '''
        if not ressie.facebook_psid:
            ressie.facebook_psid = sender_psid
            ressie.save()
        '''
    except Exception as excp: # pylint: disable=broad-except
        print(Exception, excp)
        traceback.print_exc()

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
