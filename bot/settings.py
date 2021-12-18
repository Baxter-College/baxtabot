# settings.py
#
# Get all environment variables

import os

if "HEROKU" in os.environ:
    DEBUG = int(os.environ.get("DEBUG"))
    PORT = int(os.environ.get("PORT"))
    PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
    OFFICER_PSIDS = [
        2066675683409458,  # James
        2054639917988805,  # Rohan
        2991096094285006,  # Josh
        3973058702707960  # Nick
    ]
    BROKER_URL = os.environ.get("REDIS_URL")
else:
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(dotenv_path=find_dotenv(), override=True)

    print("In a local environment!")
    DEBUG, PORT = None, None
    # DEBUG = os.environ["DEBUG"]
    # PORT = os.environ["PORT"]
    PAGE_ACCESS_TOKEN = None
    OFFICER_PSIDS = []  # [os.environ["DEBUG_PSID"]]  # current developer's psid

    BROKER_URL = "redis://"

VERIFY_TOKEN = "GoodLordyThomasJHillLooksFineTonight"
OFFICERS = "Tash or Nick"

DATE_LOCATIONS = [
    "22 Grams Coffee",
    "Village Coffee",
    "White House",
    "Roundy",
    "The Rege",
]

rohan_pub_key = b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDACFWiCZzBb9diXHp3Evj3GyH4\nX6uS+EwoKWCGaAM+/foqSKVxBRpPPEeZ05RmJ56b0bt/fdg0dxYcdS6q0ByG/AEL\nB3TKSWt6dM4D+S+JG0z4lbUkaQQ9XAiq4Mk/uyHYMe/oSYlt/Nx83hb06bXl9j/c\ncmEBUsVvLqPfXpjlSQIDAQAB\n-----END PUBLIC KEY-----'
