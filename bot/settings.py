# settings.py
#
# Get all environment variables

import os

if "HEROKU" in os.environ:
    DEBUG = int(os.environ.get("DEBUG"))
    PORT = int(os.environ.get("PORT"))
    PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
    OFFICER_PSIDS = [
        2290632767645607,
        2066675683409458,
        2054639917988805,
    ]  # tom, james, rohan
else:
    from dotenv import load_dotenv

    load_dotenv()

    print("In a local environment!")

    DEBUG = os.environ["DEBUG"]
    PORT = os.environ["PORT"]
    PAGE_ACCESS_TOKEN = os.environ["PAGE_ACCESS_TOKEN"]
    OFFICER_PSIDS = [1821155224639424]  # tom

VERIFY_TOKEN = "GoodLordyThomasJHillLooksFineTonight"
OFFICERS = "James, Rohan or Tom"

