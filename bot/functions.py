# functions.py
#
# Includes all non-messaging functionality of baxterbot

import datetime
import random
import json
import requests
import math
import mammoth
import re

from bot.settings import *

import bot.models as models


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
    # replace some encoded characters with what they should be
    # also remove all newline characters
    subs = {"&amp;": "&", "\\x96": "-", "\n|\r\n|\r|\xa0": "", "\\x92": "'"}

    for sub, repl in subs.items():
        lines = re.sub(sub, repl, lines)

    # find every table element in the html file, read each of these strings into a list
    # (also find every gap between the table elements)
    # the gaps may also contain important elements so they are treated like tables

    tables = []
    cur = 0

    match = re.search(r"<table|$", lines[cur:])
    tables.append(lines[cur : cur + match.start()])
    # the first "table" or "row" contains all header and file info up to the first table
    # this is not being used as of version 1.0 of dinoparser

    # move the search index to the index of the start of the found table
    cur += match.start()

    test = []
    while cur < len(lines):
        match = re.search(r"</table>", lines[cur:])
        if match == None:
            print("ERROR table not closed")
        tables.append(lines[cur : cur + match.end()])
        cur += match.end()

        match = re.search(r"<table", lines[cur:])
        if match == None:
            # there are no more tables, enter the remainder of the file as the last "table"
            match = re.search(r"$", lines[cur:])
        tables.append(lines[cur : cur + match.start()])
        cur += match.start()
    rows = []
    for table in tables:
        if table.startswith("<table"):
            # break all table elements down into rows
            row = re.findall(r"<tr.+?</tr>", table)
            rows += row
            # all rows are added to rows independent of their table grouping, yet order is preserved
        else:
            rows.append(table)
            # gaps are added as a single row

    elements = []
    for row in rows:
        if row.startswith("<tr"):
            # rows are split into their individual row cells/elements
            elements.append(re.findall(r"<td.+?</td>", row))
        else:
            # gaps are added as a single-cell row
            elements.append([row])

    paras = []
    for row in elements:
        newrow = []
        for ele in row:
            ps = [i[1:-1].strip() for i in re.findall(r">[^<]+?<", ele)]
            # everything between a ">" and a "<" is assumed to be information visible to a viewer
            # hence it is stored
            texts = []
            for p in ps:
                if p != "" and p != "&nbsp;":
                    # ignore all empty texts and space markers
                    texts.append(p)

            # **** do not omit empty elements ([]) as this signify an empty table cell
            # 		This means the cell inherits the value of a neighbouring cell
            # 		Information is not used as of v 1.0, however if meals want to be separated into
            # 		main/veg/salad etc this is needed
            newrow.append(texts)
        paras.append(newrow)

    mealsByDay = [[[]] for i in range(7)]

    # this stores all the sublabels for the meals (main, vegetarian, salad, desert)
    # this info is not currently used v1.0
    mealLabels = []

    # stores the dates that the menu is for, relies on the fact that the dates are the
    # first element of the second 'row' (first table row_)
    startDate = " ".join(paras[1][0])

    # stores the days of the week as listed along the top
    days = paras[1][1:]

    mealIndex = [
        "breakfast",
        "lunch",
        "dinner",
        "brekfast",
        "brekkie",
        "launch",
        "diner",
        "dinenr",
        "beakfast",
    ]
    curMeal = 0
    mealKnown = False
    mealValue = ""

    for row in paras[2:]:
        if len(row) == 0 or len(row[0]) == 0:
            continue
        if row[0][0].lower() in mealIndex:
            for i in range(7):
                mealsByDay[i].append([])
            curMeal += 1
            continue
        if (" ".join(row[0])).lower().startswith("special"):
            # last line often refers to special dietary requirements, no useful information after
            break
        mealLabel = " ".join(row[0])
        mealLabels.append(mealLabel)
        if mealLabel.lower().startswith("continental"):
            # ignore the line explaining what a continental breakfast is
            continue
        if len(row) < 2:
            continue
        for day, ele in enumerate(row[1:]):
            # add each meal into a new list which orders the individual meals by their day and then
            # by which meal of the day
            mealsByDay[day][curMeal].append(" ".join(ele))

    datesplit = re.findall(r"\w+", startDate)
    year = None
    if re.search(r"\D", datesplit[-1]) == None and len(datesplit) >= 3:
        # all integers in last position
        year = int(datesplit[-1])
    else:
        print("no year found")

    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]
    month = None
    for (i, month) in enumerate(months):
        if datesplit[-2].lower() == month:
            month = i + 1
            break

    day = None
    if re.search(r"\D", datesplit[0]) == None:
        day = int(datesplit[0])
    else:
        print("no day found")

    try:
        date = datetime.date(year, month, day)

    except:
        date = datetime.date.today()
    dates = []
    for i in range(7):
        delta = datetime.timedelta(days=i)
        dates.append(date + delta)
    return [dates, mealsByDay]

