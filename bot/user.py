from bot.models import Client, ActiveTokens


def user_update(token, email, dietaries, roomshown):
    user = Client.select().join(ActiveTokens).where(
        ActiveTokens.token == token).get()
    user.email = email
    user.dietaries = dietaries
    user.roomshown = roomshown if roomshown else False
    user.save()


def user_profile(token):
    return Client.select(Client.id, Client.name, Client.email, Client.position,
                         Client.dietaries, Client.roomshown).join(ActiveTokens).where(ActiveTokens.token == token).dicts()[0]
