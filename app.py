'''
app.py

Where the magic happens
HTTP layer + server for Baxtabot

Contributors: Tom Hill, Rohan Maloney, Nick Patrikeos
'''


import secrets
import re
import argparse
import os

# from binascii import unhexlify
# from Crypto.Hash import SHA256
# from Crypto.Signature import pkcs1_15
# from Crypto.PublicKey import RSA

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
)

from bot.settings import DEBUG, PORT
from bot.error import InputError
import bot.models as models
import bot.message as message
import bot.functions as functions
import bot.auth as auth
import bot.latemeals as latemeals
import bot.calendar as calendar
import bot.user as user
import bot.users as users
import bot.webhook as webhook
import bot.dino as dino
import bot.ressies as ressies

from bot.error import InputError

SIGN_TOKEN = secrets.token_hex(16)

app = Flask(__name__)

def authenticate_page(token, page):
    if token is None or not auth.authenticate_token(token):
        return render_template('index.html')
    if not functions.validateTokenPermissions(token, page):
        return render_template('homepage.html', permission_denied = True, token=token)

    return False

@app.before_request
def before_request():
    models.db.connect()


@app.after_request
def after_request(response):
    models.db.close()
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/admin')
def admin():
    token = request.args.get('token')

    if token and auth.authenticate_token(token):
        return render_template('homepage.html', token=token, permission_denied=False)

    return render_template('index.html')

@app.route('/logout')
def logout():
    token = request.args.get('token')

    if token and auth.authenticate_token(token):
        functions.deleteActiveToken(token)

    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        form = request.form
        # form = request.json
        email = form['email']
        password = form['password']
        name = form['name']
        print('registering', email, password)

        try:
            result = auth.auth_register(email, password, name)
            # Set token into local storage
        except InputError:
            return render_template('index.html')
        else:
            url = url_for('admin') + '?token=' + result['token']
            return redirect(url)
    else:
        return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    form = request.form
    email = form['email']
    password = form['password']
    print('logging in as', email, password)

    try:
        result = auth.auth_login(email, password)
    except InputError:
        return render_template('index.html')
    else:
        url = url_for('admin') + '?token=' + result['token']
        return redirect(url)

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route('/latemeals')
def latemeals_all():
    token = request.args.get('token')
    page = authenticate_page(token, 'latemeals')

    if not page:
        outstanding_meals = latemeals.latemeals_oustanding()
        completed_meals = latemeals.latemeals_completed()
        return render_template(
            'latemeals.html', outstandingMeals=outstanding_meals,
            completedMeals=completed_meals, token=token
        )

    return page


@app.route('/users')
def users_all():
    token = request.args.get('token')
    page = authenticate_page(token, 'users')

    if not page:
        user_list = users.users_all()
        return render_template('users.html', users=user_list, token=token)

    return page

@app.route('/user/delete', methods=['GET'])
def user_delete():
    token = request.args.get('token')
    page = authenticate_page(token, 'users')
    client_id = int(request.args.get('client_id'))

    if not page:
        users.user_delete(client_id)
        user_list = users.users_all()
        return render_template('users.html', users=user_list, token=token)

    return page


@app.route('/user/update', methods=['POST'])
def user_update():
    form = request.form

    client_id = form['client_id']
    position = form['position']
    # print(position)

    dinoread = form.get('dinoread')
    dinowrite = form.get('dinowrite')
    _calendar = form.get('calendar')
    _sport = form.get('sport')
    _latemeals = form.get('latemeals')
    _ressies = form.get('ressies')
    _users = form.get('users')
    token = form.get('token')
    page = authenticate_page(token, 'users')
    # print(client_id, token)

    if not page:
        users.user_update(client_id, position, dinoread,
                        dinowrite, _calendar, _latemeals,
                        _sport, _ressies, _users)

        user_list = users.users_all()
        return render_template('users.html', users=user_list, token=token)

    return page

@app.route('/user/profile', methods=['POST', 'GET'])
def profile():
    token = request.args.get('token')

    if token is None or not auth.authenticate_token(token):
        return render_template('index.html')

    if request.method == 'POST':
        form = request.form

        email = form['email']
        dietaries = form['dietaries']
        roomshown = form.get('roomshown')
        user.user_update(token, email, dietaries, roomshown)

    client = user.user_profile(token)
    outstanding_meals = latemeals.latemeals_oustanding_resident(client['id'])

    return render_template('profile.html', user=client,
                            token=token, outstandingMeals=outstanding_meals)

## This code needs reviewing
# pylint: disable=pointless-string-statement
'''
@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":

        response = {"text": request.form["message"]}

        for user in models.Sender.select():
            message.callSendAPI(user.psid, response)

        return render_template("update.html")
    return render_template("update.html")
'''

@app.route("/webhook", methods=["POST", "GET"])
def webhook_receive():
    return webhook.process(request)

## THIS CODE NEEDS REVIEWING

# pylint: disable=pointless-string-statement
'''
@app.route("/loveorla", methods=["GET","POST"])
def love():
    if request.method == "GET":
        global SIGN_TOKEN
        SIGN_TOKEN = secrets.token_hex(16)
        return render_template("verify.html", token=SIGN_TOKEN  )
    else:
        signature = request.form["signature"]
        content = request.form["content"]
        print("sig", signature)
        signature = unhexlify(signature.encode('utf-8'))
        digest = SHA256.new()
        digest.update(SIGN_TOKEN.encode('utf-8'))
        pub_key = RSA.import_key(rohan_pub_key)
        verifier = pkcs1_15.new(pub_key)
        try:
            verifier.verify(digest, signature)
            message.massMessage(content)
            return "Valid Signature"
        except Exception as e:
            print(e)
            return "Invalid signature"
'''

# ====== Upload Asset ====== #


@app.route("/calendar", methods=["GET"])
def calendar_page():
    token = request.args.get('token')

    page = authenticate_page(token, 'calendar')
    print(page)

    if not page:
        assets = calendar.calendars_all()
        return render_template("calendar.html", assets=assets, token=token)

    return page


@app.route("/calendar/upload", methods=["POST"])
def upload():
    token = request.form['token']

    page = authenticate_page(token, 'calendar')
    print(page)

    if not page:
        url = request.form["assetURL"]
        date = request.form['date']

        calendar.calendar_upload(url, date)

        return redirect(url_for('calendar_page') + '?token=' + token)

    return page

# ====== Add a meal ====== #

@app.route("/dino")
def dino_menu():
    token = request.args.get('token')
    writepage = authenticate_page(token, 'dinowrite')
    readpage = authenticate_page(token, 'dinoread')
    meals = dino.meals_all()

    if not writepage:
        return render_template("dinowrite.html", meals=meals, token=token)

    elif not readpage:
        return render_template("dinoread.html", meals=meals, token=token)

    return readpage


@app.route("/dino/delete", methods=["GET"])
def meal_delete():
    token = request.args.get('token')
    meal_id = request.args.get('meal_id')
    page = authenticate_page(token, 'dinowrite')

    if not page:
        dino.meals_delete(meal_id)
        return redirect(url_for("dino_menu") + '?token=token')
    return page

@app.route('/latemeals/delete', methods=['GET'])
def latemeal_delete():
    token = request.args.get('token')
    meal_id = request.args.get('meal')
    from_page = request.args.get('from')
    if from_page is None:
        page = authenticate_page(token, 'dinowrite')
    else:
        page = False

    if not page:
        latemeals.latemeal_delete(meal_id)

        if from_page is None:
            return redirect(url_for('latemeals_all') + '?token=' + token)
        return render_template('homepage.html', token=token, permission_denied=False)

    return page

@app.route("/dino/batchdelete", methods=["POST"])
def batch_delete_meal():
    form = request.form
    token = form['token']
    page = authenticate_page(token, 'dinowrite')

    if not page:
        for meal in form.getlist("delete"):
            meal_id = int(meal)
            dino.meals_delete(meal_id)

        return redirect(url_for("dino_menu") + '?token=' + token)
    return page

@app.route('/latemeals/batchcompleted', methods=['POST'])
def latemeals_batch_complete():
    form = request.form
    token = form['token']
    page = authenticate_page(token, 'dinowrite')

    if not page:
        for meal_id in form.getlist('complete'):
            latemeals.latemeals_setcompleted(int(meal_id))

        return redirect(url_for('latemeals_all') + '?token=' + token)
    return page

@app.route("/dino/fileadd", methods=["GET", "POST"])
def upload_file():
    token = request.form['token']
    page = authenticate_page(token, 'dinowrite')

    if not page:
        if request.method == "POST":
            # check if the post request has the file part
            if "file" not in request.files:
                print("No file part")
                return redirect(request.url)

            file = request.files["file"]
            # if user does not select file, browser also
            # submit an empty part without filename

            if file.filename == "":
                print("No selected file")
                return redirect(request.url)

            if file.filename.endswith(".docx"):
                extracted = dino.file_extract_docx(file)
                return render_template("checkParser.html", extracted=extracted)

            if file.filename.endswith(".html") or file.filename.endswith(".htm"):
                meals_by_day = dino.file_extract_html(file)
                return render_template("checkParser.html", mealsByDay=meals_by_day)

        else:
            return redirect(url_for("dino_menu") + '?token=' + token)
    return page

@app.route("/dino/file/confirm", methods=["POST"])
def confirm_file():
    form = request.form
    meals = ["breakfast", "lunch", "dinner"]

    for day in range(1, 8):
        date = form[str(day) + "/" + "date"]

        for meal in range(1, 4):
            things = form.getlist(str(day) + "/" + str(meal))
            description = "\n\n".join(things)

            subs = {
                "&amp;": "&", "\\x96": "-",
                "\\x92": "'", "\\u2019":"'",
                "\\u2018":"'", "\\u2013": "-"
            }

            for sub, repl in subs.items():
                description = re.sub(sub, repl, description)
            print("\n\n here we go:", date, "\n\ndescr: ", description, "\n\nmeal", meals[meal - 1])

            dino.meals_add(date, description, meals[meal - 1])

    return redirect(url_for("admin"))


# ======= Resident Information ======= #
@app.route("/ressie", methods=["POST", "GET"])
def resident():
    token = request.args.get('token') if request.method == 'GET' else request.form['token']
    page = authenticate_page(token, 'ressies')

    if not page:
        if request.method == "POST":
            # do resident creation
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            room_number = request.form['room_number']

            ressies.ressie_create(first_name, last_name, room_number)

        ressie_list = ressies.ressies_all()
        return render_template("ressie.html", ressies=ressie_list, token=token)
    return page

@app.route('/ressie/fileadd', methods=['GET', 'POST'])
def upload_residents():
    payload = request.form
    token = payload['token']

    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file given.')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        ressies.file_upload(file)

    return redirect(url_for('resident') + '?token=' + token)

@app.route("/ressie/delete/<int:ressie_id>", methods=["GET"])
def ressie_delete(ressie_id):
    token = request.args.get('token')

    page = authenticate_page(token, 'ressies')
    if not page:
        ressies.ressie_delete(ressie_id)
        ressie_list = ressies.ressies_all()
        return render_template("ressie.html", ressies=ressie_list, token=token)

    return page

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--terminal", help="Run Baxtabot in the terminal", action="store_true"
    )
    args = parser.parse_args()

    models.goGoPowerRangers()
    message.resetBot()

    if args.terminal:
        while True:
            msg = str(input("> ")) # pylint: disable=invalid-name
            print("BAXTABOT: ", message.handleMessage("cmd", msg)["message"]["text"])
    else:
        os.system('NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program')
        app.run(debug=DEBUG, port=PORT, host="0.0.0.0")
