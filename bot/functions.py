# functions.py
#
# Includes all non-messaging functionality of baxterbot

import datetime
from dateutil.parser import *
import random
import json
import requests
import math
import mammoth
import re
from bs4 import BeautifulSoup

from bot.settings import *

import bot.models as models
import bot.extract as extract


# ====== Specific functions ===== #
def findMeal(message):
    if "dinner" in message:
        meal = "dinner"
    elif "lunch" in message:
        meal = "lunch"
    elif "breakfast" in message:
        meal = "breakfast"

    return meal


def findTime(message):

    addTime = datetime.timedelta(hours=0)

    today = datetime.datetime.today() + datetime.timedelta(hours=11)
    days = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    if "tomorrow" in message or "tommorow" in message:
        addTime += datetime.timedelta(hours=24)

    for day in days:
        if day in message:  # if the day is mentioned
            dayDiff = days[day] - today.weekday()  # get difference between days
            if dayDiff < 0:  # if the day is "behind" current day, make day next week
                dayDiff += 7
            elif "next" in message:
                addTime += datetime.timedelta(hours=24 * 7)  # add this day next week

            addTime += datetime.timedelta(hours=24 * dayDiff)

    return addTime


def dinoRequest(meal, addTime):
    # meal is "dinner", "lunch" or "breakfast"

    ten_hours = datetime.timedelta(hours=11)

    today = datetime.datetime.now()

    today_AEST = today + ten_hours

    today_AEST += addTime  # if no add time, timedelta will be 0 hours so no effect

    print("Date is: {}".format(today_AEST.date().strftime("%Y-%m-%d")))

    try:
        dino = (
            models.Meal.select()
            .where(models.Meal.date == today_AEST.date())
            .where(models.Meal.type == meal)
            .get()
        )
    except Exception as e:
        print("---> ", e)
        print("Meal: ", meal)
        print("Date: ", today_AEST.date())
        return "Honestly.... I don't know."

    return "{} at dino is:\n{}".format(meal, dino.description)

def dinoRequestObj(meal, addTime):
    # meal is "dinner", "lunch" or "breakfast"

    ten_hours = datetime.timedelta(hours=11)

    today = datetime.datetime.now()

    today_AEST = today + ten_hours

    today_AEST += addTime  # if no add time, timedelta will be 0 hours so no effect

    print("Date is: {}".format(today_AEST.date().strftime("%Y-%m-%d")))

    try:
        dino = (
            models.Meal.select()
            .where(models.Meal.date == today_AEST.date())
            .where(models.Meal.type == meal)
            .get()
        )
    except Exception as e:
        return None

    return dino


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

    if dino.likes == 0 and dino.dislikes == 0:
        message = "No one has voted for {}! 😢\nYou can be the first to vote with 'dinovote'".format(
            dino.type
        )

    elif dino.likes < dino.dislikes:
        perc = (dino.dislikes / (dino.dislikes + dino.likes)) * 100
        message = "{}% of people disliked {}.".format(perc, dino.type)

    elif dino.likes > dino.dislikes:
        perc = (dino.likes / (dino.dislikes + dino.likes)) * 100
        message = "{}% of people enjoyed {}!!!".format(perc, dino.type)

    else:
        message = "The crowd is split! Dino is a polarising meal.\nLet me know your thoughts with 'dinovote'"

    return message


def getCurrentDino():

    time = datetime.datetime.now() + datetime.timedelta(hours=11)  # to make it aest

    today = datetime.datetime.today() + datetime.timedelta(hours=11)
    breakfast = today.replace(hour=7, minute=0)
    lunch = today.replace(hour=12, minute=0)
    dinner = today.replace(
        hour=16, minute=0
    )  # just to make sure (starting at 4 so people can ask what's dino earlier for dinner)

    try:
        if time < lunch:
            # for today's breakfast
            dino = (
                models.Meal.select()
                .where(models.Meal.type == "breakfast")
                .where(models.Meal.date == today.date())
                .get()
            )
        elif time >= lunch and time < dinner:
            # for today's lunch
            dino = (
                models.Meal.select()
                .where(models.Meal.type == "lunch")
                .where(models.Meal.date == today.date())
                .get()
            )
        elif time >= dinner:
            # for today's dinner
            dino = (
                models.Meal.select()
                .where(models.Meal.type == "dinner")
                .where(models.Meal.date == today.date())
                .get()
            )
        return dino
    except:
        return None


# ======== J&D ========== #


def set_jd(rs, switch):

    jd_desc = ""

    try:
        if switch[1]:
            message.bot.set_variable("jd_loc", switch[1])
            jd_desc = " in the {}".format(switch[1])
    except:
        message.bot.set_variable("jd_loc", None)

    if switch[0].lower() == "on":
        message.bot.set_variable("jd", True)
        # jd = True
        return "COFFEE TIME!!! ☕️\nJ&D is ON" + jd_desc
    else:
        message.bot.set_variable("jd", None)
        message.bot.set_variable("jd_loc", None)
        return "No more coff! 😭"


def get_jd(rs, args):

    jd = message.bot.get_variable("jd")
    jd_loc = message.bot.get_variable("jd_loc")

    jd_desc = ""

    if jd_loc:
        jd_desc = " in the {}".format(jd_loc)

    if jd:
        return "J&D is ON" + jd_desc
    else:
        return "J&D is OFF 😭 😭 😭"


# ===== Shopen ===== #

# TODO: integrate this toggle action into a function so we are not duplicating functionality


def set_shop(rs, switch):

    if switch[0].lower() == "on":
        message.bot.set_variable("shop", True)
        return "Shopen!"
    else:
        message.bot.set_variable("shop", None)
        return "Shclosed 😭"


def get_shop(rs, args):

    shop = message.bot.get_variable("shop")

    return "Shopen!!!" if shop else "Shclosed 😭"


# ===== Baxter Events ===== #
# TODO: Move this into message module
def uploadAsset(assetUrl):

    r = requests.post(
        "https://graph.facebook.com/v2.6/me/message_attachments",
        params={"access_token": PAGE_ACCESS_TOKEN},
        json={
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {"is_reusable": True, "url": assetUrl},
                }
            }
        },
    )

    if r.status_code == 200:
        return r.json()
    else:
        print("Asset Upload has gone to shit -> ", r.status_code)
        return None


# ===== Hashbrowns ===== #

def set_hashbrowns(rs, switch):

    message.bot.set_variable('hashbrownsday', datetime.date.today())
    if switch[0].lower() == 'on':
        message.bot.set_variable('hashbrowns', True)
        return "OMG best news ever! 😃 Your friends will arrive shortly..."
    else:
        message.bot.set_variable('hashbrowns', None)
        return "N-n-n-noooooooo! 😭 Enjoy a lonely Dino, knowing you took one for the team..."

def get_hashbrowns(rs, args):

    if (message.bot.get_variable('hashbrownsday') == datetime.date.today()):
        hashbrowns = message.bot.get_variable('hashbrowns')
        return "Get out of bed! HASHBROWNS TODAY!!! 🥔🥔🎊🎉🎊🎉" if hashbrowns else "Bad news: no hashbrowns... stay in bed 😔"
    else:
        return "Nobody's been game to find out yet 🤔 Type 'sethashbrowns on' or 'sethashbrowns off' if you happen to get out of bed"


# ======= Semester In Progress ======= #
def semesterResponse():

    # is this hardcoded? yes.
    # do i give a shit? no. fuck you for judging me.
    semStart = datetime.date(2019, 5, 31)
    semEnd = datetime.date(2019, 9, 2)

    response = "{}\n\nThere are {} days left until the semester ends".format(
        progressBar(timeProgress(semStart, semEnd)), daysLeft(semEnd)
    )

    return response


def yearProgress():
    today = datetime.datetime.today() + datetime.timedelta(hours=11)  # to make it aest

    percentage = math.floor((today.timetuple().tm_yday / 365) * 100)

    return percentage


def timeProgress(start, end):
    today = datetime.datetime.today() + datetime.timedelta(hours=11)  # to make it aest

    totalDays = (end - start).days
    elapsedDays = (today.date() - start).days

    percentage = math.floor((elapsedDays / totalDays) * 100)

    return percentage


def daysLeft(end):
    today = datetime.datetime.today() + datetime.timedelta(hours=11)  # to make it aest

    return (end - today.date()).days


def progressBar(percentage):

    percBar = "0% "

    for i in range(10, 100, 10):
        percBar += "▓" if (i < percentage) else "░"

    percBar += " {}%".format(percentage)

    return percBar


# ===== Week Events ===== #
def getWeekEvents():

    today = datetime.datetime.today() + datetime.timedelta(hours=11)  # to make it aest
    # Take todays date. Subtract the number of days which already passed this week (this gets you 'last' monday).
    week_monday = today + datetime.timedelta(days=-today.weekday(), weeks=0)

    try:
        weekCal = (
            models.WeekCal.select()
            .where(models.WeekCal.week_start == week_monday.date())
            .get()
        )

        return weekCal.assetID
    except:
        return None


# ===== Get Room Number ===== #
def extractName(msg):
    half = msg.split("is", 1)[1].split()
    return " ".join(half[:2])


def getRoomNumber(name):

    try:
        gotName, confidence, ressie = models.Ressie.fuzzySearch(name)
        if confidence < 85:
            return "{} is in room {} (I'm {} percent sure I know who you're talking about)".format(
                gotName, ressie.room_number, confidence
            )
        return "{} is in room {}".format(gotName, ressie.room_number)
    except:
        return """I could not find a room number for '{}' ... are you sure they go to Baxter?
          \nPlease make sure you spell their full name correctly.\n\n (Fun fact: Some people use names that are not in fact their names. Nicknames won't work)""".format(
            " ".join(name).title()
        )

def dinoparse(lines):
    extract.text_replace(lines)

    soup = BeautifulSoup(lines, features="html.parser")
    assert soup != None
    pretty = soup.prettify()

    tables = soup.find_all('table')
    curMeal = 0
    dateStr = ""
    first_row = tables[0].find('tr')
    dateCol = first_row.find('td')
    dateStr = dateCol.get_text()
    for table in tables:
        tbody = table.find('tbody')
        #assert tbody != None
        rows = table.find_all('tr')

        rowSpans = {}

        for rownum, row in enumerate(rows[1:]):
            cols = row.find_all('td')
            heading = ""
            delta = 0
            for ind, col in enumerate(cols):
                if str(rownum) in rowSpans and ind in rowSpans[str(rownum)]:
                    rowSpans[str(rownum)].remove(ind)
                    delta += 1
                colnum = ind + delta
                if col.has_key('rowspan'):
                    rowspan = int(col['rowspan'])
                    for i in range(1, rowspan):
                        key = str(rownum + i)
                        if key in rowSpans:
                            rowSpans[key].append(colnum)
                        else:
                            rowSpans[key] = [colnum]
                    
                string = col.get_text()
                if string == "":
                    continue
                if colnum == 0:
                    if curMeal < 3 and any([i in string for i in mealTitles[curMeal]]):
                        print("meal found:")
                        print(string)
                        curMeal += 1
                        for i in range(7):
                            mealsByDay[i].append([])
                        break
                    if any([string.lower().startswith(i) for i in ignoredRows]):
                        break
                    heading = string.strip().capitalize()
                    continue
                    
                day = colnum - 1
                mealsByDay[day][curMeal].append(heading + ":\n" + string)
    dateStr = dateStr.split('-')[0]
    date = parse(dateStr)
    if date == None:
        date = datetime.date.today()
    dates = [(date + datetime.timedelta(days=i)).date() for i in range(7)]
    return [dates, mealsByDay]

