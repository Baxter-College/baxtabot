import bot.models as models
import hashlib
from uuid import uuid4
import re

class AuthException(Exception):
    pass

def authenticate_token(token):
    found = models.ActiveTokens.select().where(models.ActiveTokens.token == token)
    if found:
        return found.get()


def auth_register(email, password, name):
    """
    Registers a new user. ####Returns their id and token.
    """

    if not isinstance(email, str) or not isinstance(password, str):
        raise AuthException(description="Input error: invalid arguments")

    if not email_valid(email):
        raise AuthException(description="Input error: email is not valid")

    # check_length(password, "password", 6, 64)
    # check_length(first, "first name", 1, 50)
    # check_length(last, "last name", 1, 50)

    # if database.Exception(email):
    #     raise AuthException(description="Input error: email is already in use")

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
        raise AuthException(description="Input error: invalid arguments")

    if not email_valid(email):
        raise AuthException(description="Input error: email is not valid")


    encoder = hashlib.sha224()
    encoder.update(password.encode('utf-8'))
    hashed_password = encoder.hexdigest()

    user = models.Client.select().where(models.Client.email == email and models.Client.password == hashed_password)

    if user is None:
        raise Exception(description="Input error: email/password is not correct")

    user = user.get()

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
        raise InputError(description="Input error: " + name + " must contain " \
                                                     + str(min_len) + " or more characters")

    if len(string) > max_len:
        raise InputError(description="Input error: " + name + " must contain " \
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

def count_duplicates(handle):
    """
    Counts the number of users with the given handle
    """

    count = 0
    if handle == "hangman": count = 1

    for user in database.users:
        if handle in (user.handle, user.original_handle):
            count += 1

    return count

def generate_handle(first, last=None, count=0):
    """
    Generates a unqie user handle based on the concatenation
    of their first and last names. Changes are made to ensure
    uniqueness and that it complies with the size limit.
    """

    if last is None:
        handle = first
    else:
        handle = first.lower() + last.lower()

    if len(handle) > User.HANDLE_MAX_LENGTH:
        handle = handle[0:User.HANDLE_MAX_LENGTH]

    original_handle = handle

    duplicate_count = count_duplicates(handle)

    if duplicate_count > 0:
        if count == 0:
            discriminator = str(duplicate_count)
        else:
            discriminator = str(count)

        possible_change = handle[0:User.HANDLE_MAX_LENGTH - len(discriminator)] + discriminator

        if count_duplicates(possible_change) > 0:
            handle, original_handle = generate_handle(possible_change, count=count + 1)
        else:
            handle = possible_change

    return (handle, original_handle)
