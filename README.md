# baxtabot

> Baxter's official sentient AI assistant!

You can message it at: [m.me/baxtabot](https://m.me/baxtabot) (Note: currently only available to registered testers)

## Setup

- Set up a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) **using pipenv** (see [pipenv docs](https://docs.pipenv.org/))

- run `python app.py`

You may need to adjust some settings such as `HOST`, `PORT` and the postgres database login details in `models.py` to run on your local machine

### Local Testing

Use the **BaxtaBot - DEV** messenger bot. Install [ngrok](https://ngrok.com/) and forward the flask server created on `localhost:5000`

Then ensure that the correct webhook url (i.e. the one created by ngrok) is being used in the facebook apps dashboard for **baxtabot - dev** (NOT PRODUCTION ONE!)

You may need to create `PAGE_ACCESS_TOKEN` as a temporary environment variable. You can get this also from the facebook apps dashboard under the dev bot.

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
	- What floor is pre's on?
	- integrate vac trac
	- When is the bus leaving?
