# baxtabot

> Baxter's official sentient AI assistant!

You can message it at: [m.me/baxtabot](https://m.me/baxtabot) (Note: currently only available to registered testers)

## Setup

- Set up a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) **using pipenv** (see [pipenv docs](https://docs.pipenv.org/))

- create a `.env` file including:
	- `DB_NAME` (postgres database name)
	- `DB_USER` (postgres username)
	- `DB_PASSWORD` (postgres password)
	- `PAGE_ACCESS_TOKEN` (find in facebook apps dashboard)
	- `DEBUG` (int, 1 or 0)
	- `PORT` (int, usually 5000)

- run `python app.py`

### Local Testing

Use the **BaxtaBot - DEV** messenger bot. Install [ngrok](https://ngrok.com/) and forward the flask server created on `localhost:5000`

Then ensure that the correct webhook url (i.e. the one created by ngrok) is being used in the facebook apps dashboard for **baxtabot - dev** (NOT PRODUCTION ONE!)
Go to **webhooks section** in facebook apps dashboard and click "edit subscription" and paste in ngrok webhook url and the verify token

You may need to create `PAGE_ACCESS_TOKEN` in your `.env` file. You can get this also from the facebook apps dashboard under the dev bot.

To add a test user, go to: developers.facebook.com/requests

## Current Functions

- simple discussions (via rivescript)
- baxter related simple discussions (via rivescript)
- ask what is for dinner/lunch/breakfast at dino
- ask to call the duty tutor
- dino voting
- is J&D on right now?

## Future

- see todo.md
- would like to implement a smarter dialog system (possibly actual machine learning rather than pattern matching?) (dialogflow??)
- some other ideas:
	- integrate vac trac
	- When is the bus leaving?
