import bot.models as models
import hashlib
from uuid import uuid4
import re

class AuthException(Exception):
    description = 'No description given'

def authenticate_token(token):
    found = models.ActiveTokens.select().where(models.ActiveTokens.token == token)
    if found:
        return found.get()


def auth_register(email, password, name):
    """
    Registers a new user. ####Returns their id and token.
    """

    if not isinstance(email, str) or not isinstance(password, str):
        raise AuthException("Input error: invalid arguments")

    if not email_valid(email):
        raise AuthException("Input error: email is not valid")

    check_length(password, "password", 6, 64)
    check_length(first, "first name", 1, 50)
    check_length(last, "last name", 1, 50)

    encoder = hashlib.sha224()
    encoder.update(password.encode('utf-8'))
    hashed_password = encoder.hexdigest()
    ressie_name, confidence, ressie = models.Ressie.fuzzySearch(name)

    if confidence > 85:
        ressie = ressie.id
        name = ressie_name
    else:
        ressie = None

    user = models.Client.create(email=email, password=hashed_password, name=name, ressie=ressie)
    models.ClientPermissions.create(client=user.id)

    print(user.id)
    token = generate_token(user.id)
    models.ActiveTokens.create(client=user.id, token=token)

    return {"u_id": user.id, "token": token}

def auth_login(email, password):
    """
    Logs an existing user in. Returns their id and token.
    """

    if not isinstance(email, str) or not isinstance(password, str):
        raise AuthException("Input error: invalid arguments")

    if not email_valid(email):
        raise AuthException("Input error: email is not valid")


    encoder = hashlib.sha224()
    encoder.update(password.encode('utf-8'))
    hashed_password = encoder.hexdigest()
    print(email)
    user = models.Client.select().where((models.Client.email == email) & (models.Client.password == hashed_password))

    try:
        user = user.get()
    except:
        raise AuthException("Input error: email/password is not correct")


    token = generate_token(user.id)
    models.ActiveTokens.create(client=user.id, token=token)

    return {"u_id": user.id, "token": token}


def auth_logout(token):
    """
    Logs an existing user out. Returns an indication of success.
    """

    if not isinstance(token, str):
        return {"is_success": False}

    if authenticate_token(token):
        models.ActiveTokens.delete().where(models.ActiveTokens.token == token)
        return {"is_success": True}

    return {"is_success": False}

'''
def auth_passwordreset_request(email):
    """
    Sends the email address an email containing a secret code to which
    can be used to reset their password through /auth/passwordreset/reset
    """
    u_id = database.get_user_by_email(email).user_id
    if (u_id == None):
        # Early return. This function should not raise any errors
        return {}

    reset_code = generate_reset_code(u_id)
    message = "Reset Code is " + reset_code

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", context=context) as email_server:
        email_server.login(HOST_EMAIL, HOST_PASSWORD)
        email_server.sendmail(HOST_EMAIL, email, message)

    return {}

def auth_passwordreset_reset(reset_code, new_password):
    """
    Given the reset code, the user's password is reset and changed to the
    new password inputted
    """
    if reset_code not in database.password_reset_codes:
        raise InputError(description="Input error: reset code is not valid")

    check_length(new_password, "password", 6, 64)

    user = database.get_user(database.password_reset_codes[reset_code])
    user.password = new_password
    del database.password_reset_codes[reset_code]

    return {}
'''

### Helper Functions ###

def email_valid(email):
    """
    Validates an email address
    """
    return re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email) is not None

def check_length(string, name, min_len, max_len):
    """
    Checks that the length of a string is between `min` and `max`.
    The argument `name` is used in the human-readable InputError
    message which is thrown if the check is failed.
    """

    if len(string) < min_len:
        raise InputError("Input error: " + name + " must contain " \
                                                     + str(min_len) + " or more characters")

    if len(string) > max_len:
        raise InputError("Input error: " + name + " must contain " \
                                                     + str(max_len) + " or less characters")

def generate_token(user_id):
    """
    Generates an auth token
    """
    token = str(uuid4())
    return token

def generate_reset_code(user_id):
    """
    Generates a reset code
    """
    reset_code = "".join(random.choices(string.ascii_uppercase + \
            string.ascii_lowercase + string.digits, k=RESET_CODE_LEN))
    database.password_reset_codes[reset_code] = user_id
    return reset_code
