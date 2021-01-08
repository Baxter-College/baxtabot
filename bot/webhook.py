import bot.message as message
from bot.settings import OFFICERS

def handle_postback(sender_psid, webhook_event):
    # handle the postback
    try:
        return message.handlePostback(
            sender_psid,
            webhook_event["postback"],
            webhook_event["message"]["text"],
        )
    except KeyError:
        print('Can\'t send images')

def handle_message(sender_psid, webhook_event):
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

def handle_post(request):
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
            if not sender:
                ### error happened and we could not resolve the identity of the sender
                return ""

            if sender.conversation and "message" in webhook_event:
                return message.handleConversation(
                    sender_psid, webhook_event["message"], sender.conversation
                )

            if "postback" in webhook_event:
                return handle_postback(sender_psid, webhook_event)
            elif "message" in webhook_event:
                return handle_message(sender_psid, webhook_event)
            else:
                return Response(
                    sender_psid,
                    text=f"I can't deal with whatever shit you just sent me. Go complain to {OFFICERS} about it",
                ).send()

    else:
        # send error
        print("Something went shit")
        return "Not Okay"

def handle_get(request):
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

def process(request):
    if request.method == "POST":
        return handle_post(request)
    elif request.method == "GET":
        return handle_get(request)
    else:
        print("Someone decided to be an idiot.")
