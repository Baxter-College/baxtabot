from bot.settings import *
import requests

from enum import Enum, auto


class Message_Tag(Enum):
    # tags and descriptions are here:
    # https://developers.facebook.com/docs/messenger-platform/send-messages/message-tags

    RESPONSE = auto()
    BUSINESS_PRODUCTIVITY = auto()
    COMMUNITY_ALERT = auto()
    CONFIRMED_EVENT_REMINDER = auto()
    NON_PROMOTIONAL_SUBSCRIPTION = auto()
    PAIRING_UPDATE = auto()
    APPLICATION_UPDATE = auto()
    ACCOUNT_UPDATE = auto()
    PAYMENT_UPDATE = auto()
    PERSONAL_FINANCE_UPDATE = auto()
    SHIPPING_UPDATE = auto()
    RESERVATION_UPDATE = auto()
    ISSUE_RESOLUTION = auto()
    APPOINTMENT_UPDATE = auto()
    GAME_EVENT = auto()
    TRANSPORTATION_UPDATE = auto()
    FEATURE_FUNCTIONALITY_UPDATE = auto()
    TICKET_UPDATE = auto()


class Response:
    def __init__(
        self,
        psid=None,
        text=None,
        image=None,
        asset=None,
        msg_type=Message_Tag.RESPONSE,
    ):
        self.psid = psid
        self.text = text
        self.image = image
        self.asset = asset
        self.quick_replies = []
        self.buttons = []

        if msg_type == Message_Tag.RESPONSE:
            self.type = Message_Tag.RESPONSE.name
        else:
            self.type = "MESSAGE_TAG"
            self.tag = msg_type.name

    def add_reply(self, reply):
        self.quick_replies.append(reply.rep)

    def add_button(self, button):
        self.buttons.append(button)

    @property
    def payload(self):
        response = {}
        if self.text:
            response["text"] = self.text

        if self.image:
            response["attachment"] = {"type": "image", "payload": {"url": self.image}}

        if self.asset:
            response["attachment"] = {
                "type": "image",
                "payload": {"assetID": self.asset},
            }

        if self.quick_replies:
            response["quick_replies"] = self.quick_replies

        if self.buttons:
            response["attachment"] = {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": self.text,
                    "buttons": [button.rep for button in self.buttons],
                },
            }
            response.pop("text")

        payload = {
            "messaging_type": self.type,
            "recipient": {"id": self.psid},
            "message": response,
        }

        if self.type == "MESSAGE_TAG":
            payload["tag"] = self.tag

        return payload

    def send(self, psid=None, timeout=None):
        """
        Sends the response to sender via facebook Send API
        """
        if not self.psid and not psid:
            Exception("You must include a PSID somewhere!")

        if not self.psid:
            self.psid = psid

        r = requests.post(
            "https://graph.facebook.com/v2.6/me/messages",
            params={"access_token": PAGE_ACCESS_TOKEN},
            json=self.payload,
            timeout=timeout
        )

        if r.status_code == 200:
            return "OK"
        return "NOT OKAY"


class Reply:
    def __init__(self, text, payload=None):
        self.text = text
        self.payload = payload

    @property
    def rep(self):
        res = {"content_type": "text", "title": self.text}
        if self.payload:
            res["payload"] = self.payload
        else:
            res["payload"] = self.text
        return res


class Button:
    def __init__(self, title):
        self.title = title

    @property
    def rep(self):
        return {"title": self.title}


class URLButton(Button):
    def __init__(self, title, url):
        super().__init__(title)
        self.url = url

    @property
    def rep(self):
        d = super().rep
        d.update({"url": self.url, "type": "web_url"})
        return d


class PostbackButton(Button):
    def __init__(self, title, payload):
        super().__init__(title)
        self.payload = payload

    @property
    def rep(self):
        d = super().rep
        d.update({"payload": self.payload, "type": "postback"})
        return d


class CallButton(Button):
    def __init__(self, title, payload):
        super().__init__(title)
        self.payload = payload

    @property
    def rep(self):
        d = super().rep
        d.update({"payload": self.payload, "type": "phone_number"})
        return d

