# baxtabot

> Baxter's official sentient AI assistant!

You can message it at: [m.me/baxtabot](https://m.me/baxtabot)

## Current Functions

- simple discussions (via rivescript)
- baxter related simple discussions (via rivescript)
- ask what is for dinner/lunch/breakfast at dino
- ask to call the duty tutor/UNSW security/lifeline
- dino voting
- ask what the week's events are
- ask what room someone is in
- is J&D on right now?

## Baxtabot Website

- View/upload dino menu
- Upload weekly calendar
- Send a message to all users (needs reviewing)
- View/upload ressie list

## Coming Soon...

- order a late meal
- register and log in to a web interface with homepage
- view my profile and add special dietary requirements/room sharing/email
- users portal to manage all registered users and permissions
- late meal portal to view all late meals ordered and mark as completed
- sport portal to upload weekly sport events
- coffee night portal to upload weekly coffee night links
- Return of is J&D on and is shopen

## Getting Started

Have you learned to code in Python and how to use Git? If not, have a look [here](python_tutorial.md).

### Account and Organisation Setup

#### GitHub

You will need to go to the [Github homepage](https://github.com/) and register an account. Once you've done that ask to be invited to the [Philip  Baxter College](https://github.com/Baxter-College/) organisation. GitHub is the platform where we upload and store all of our code. 

#### Heroku

After Github you will need to go to the [Heroku website](https://id.heroku.com/login) and register an account. Then ask to be added to the baxtabot and baxtabot-dev projects. Heroku is what deploys our code and allows people to actually use baxtabot over the internet (either through the website or by messaging the app).

#### Facebook Developers

Register an account at [Facebook Developers](https://developers.facebook.com) and ask to be added to the Baxtabot project. This platform isn't used for much except looking at analytics for people messaging the bot. Make sure you can also access Baxtabot - Dev. Once you've been added you should also be an administrator on the facebook pages themselves (they should appear on your pages).

#### Facebook

Ask to be added to the Baxtabot and Baxtabot - DEV facebook pages as an editor. You'll be able to see what messages people send 😈 !!

#### Baxtabot

Make sure you have registered an account on the [Baxtabot system](http://baxtabot.herokuapp.com). 

### Git Repository

Go to the repository homepage (if you're reading this then you're on it) and clone the repo onto your computer. Presto! You're ready to start becoming an xtreme coder.

### Make Your First Feature

Baxtabot has two seperate platforms - the blue one, which is what people use (i.e. the production version) and the pink one, which is what we use to develop and test features (i.e. the test version). The pink one is called Baxtabot - DEV. You should be able to message the blue and the pink ones on Facebook and receive the same response from both. 

Both the Dev and Production bots are connected to the same repository. Whenever you first make a change whatever you do *don't* just `git push`, otherwise you could accidentally break the live version which is bad.

To make your first change switch to a new branch called `yourname_rive` and then go inside `bot/brain` and into `baxter.rive`. At the bottom of the file, create a new entry. Here's an example:

```
+ [*] 2021 [*]
- 2021, here we come! Let's hope it's a whole lot better than 2020.
```

Don't include uppercase letters in the part after the + sign.

Once you've done that make sure to git add and commit. Then type:

```
git push origin yourname_rive:dev --force
```

What this will do is a *force push* of your changes to the `dev` branch. You need to do a force push otherwise you may need to pull someone else's changes that they are still developing/testing and cause the app to crash. When you push to the `dev` branch, Heroku has been configured to automatically deploy the updated branch to baxtabot-dev. This means that when you text the DEV bot, it will have your change!

After you force push go to the baxtabot-dev panel on Heroku and watch as the new version builds and then deploys. Once it's deployed you can text the DEV bot and it should respond as you've programmed it to!

Got that working? Well done, you've made your first feature!!

### Deploying to Production

When you make a feature and are happy that it is ready to be put into the main bot that everyone uses, you will need to make a pull request on GitHub (under the pull requests tab) where the source branch is `dev` and the target branch is `master`. Someone else will need to peer review your pull request before you can merge it in. When you merge in, `master` will automatically deploy to baxtabot on Heroku - meaning that your new feature will be out there for everyone to use!

## Setup - Old

- Set up a [virtual environment](https://docs.python-guide.org/dev/virtualenvs/) **using pipenv** (see [pipenv docs](https://docs.pipenv.org/))

- create a `.env` file including: - `DB_NAME` (postgres database name) - `DB_USER` (postgres username) - `DB_PASSWORD` (postgres password) - `PAGE_ACCESS_TOKEN` (find in facebook apps dashboard) - `DEBUG` (int, 1 or 0) - `PORT` (int, usually 5000)

- run `python app.py`

### Local Testing

You can test in the terminal by adding the `--terminal` parameter (`python3 app.py -t`) - images obviously won't work.

Use the **BaxtaBot - DEV** messenger bot. Install [ngrok](https://ngrok.com/) and forward the flask server created on `localhost:5000`

Then ensure that the correct webhook url (i.e. the one created by ngrok) is being used in the facebook apps dashboard for **baxtabot - dev** (NOT PRODUCTION ONE!)
Go to **webhooks section** in facebook apps dashboard and click "edit subscription" and paste in ngrok webhook url and the verify token

You may need to create `PAGE_ACCESS_TOKEN` in your `.env` file. You can get this also from the facebook apps dashboard under the dev bot.

To add a test user, go to: developers.facebook.com/requests

### Make sure Nick adds you to all of these

* [ ] GitHub Philip Baxter College Organisation
* [ ] Baxtabot Facebook Page
* [ ] Baxtabot - Dev Facebook Page
* [ ] Baxtabot Facebook for Developers
* [ ] Baxtabot - Dev Facebook for Developers
* [ ] Heroku 
* [ ] Heroku-Dev 

## Future

- see todo.md
- would like to implement a smarter dialog system (possibly actual machine learning rather than pattern matching?) (dialogflow??)
- some other ideas: - integrate vac trac - When is the bus leaving?

