import bot.models as models

def clear():
    q1 = models.ActiveTokens.delete()
    q2 = models.ClientPermissions.delete()
    q3 = models.Client.delete()
    q1.execute()
    q2.execute()
    q3.execute()
