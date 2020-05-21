# settings.py
#
# Get all environment variables

import os

if "HEROKU" in os.environ:
    DEBUG = int(os.environ.get("DEBUG"))
    PORT = int(os.environ.get("PORT"))
    PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
    OFFICER_PSIDS = [
        2066675683409458,
        2054639917988805,
    ]  # james, rohan
else:
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(dotenv_path=find_dotenv(), override=True)

    print("In a local environment!")

    DEBUG = os.environ["DEBUG"]
    PORT = os.environ["PORT"]
    PAGE_ACCESS_TOKEN = os.environ["PAGE_ACCESS_TOKEN"]
    OFFICER_PSIDS = [os.environ["DEBUG_PSID"]]  # current developer's psid

VERIFY_TOKEN = "GoodLordyThomasJHillLooksFineTonight"
OFFICERS = "James, Rohan or Tom"

DATE_LOCATIONS = [
    "22 Grams Coffee",
    "Village Coffee",
    "White House",
    "Roundy",
    "The Rege",
]

