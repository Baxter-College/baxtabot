from bot.models import Client, ClientPermissions

def users_all():
    user_list = Client.select(Client.id, Client.ressie, Client.name, Client.email, Client.position, ClientPermissions.dinoread,
                                ClientPermissions.dinowrite, ClientPermissions.calendar, ClientPermissions.latemeals,
                                ClientPermissions.ressies, ClientPermissions.sport, ClientPermissions.users).join(ClientPermissions).dicts()

    return user_list

def user_update(client_id, dinoread, dinowrite, calendar, latemeals, sport, ressies, users):
    userperms = models.ClientPermissions.select().where(models.ClientPermissions.client == client_id).get()
    user = models.Client.select().where(models.Client.id == client_id).get()
    user.position = position
    # print(user.position, position)
    userperms.dinoread = dinoread if dinoread else False
    userperms.dinowrite = dinowrite if dinowrite else False
    userperms.calendar = calendar if calendar else False
    userperms.latemeals = latemeals if latemeals else False
    userperms.sport = sport if sport else False
    userperms.ressies = ressies if ressies else False
    userperms.users = users if users else False
    userperms.save()
    user.save()


def user_delete():
    token = ActiveTokens.select().where(ActiveTokens.client == client_id)

    if token:
        token = token.get()
        token.delete_instance()

    perms = ClientPermissions.select().where(ClientPermissions.client == client_id).get()
    perms.delete_instance()

    client = Client.select().where(Client.id == client_id).get()
    client.delete_instance()
