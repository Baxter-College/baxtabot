# To Do - 2021

## 2.0.0 (New Release)

### Functionality

- [ ] Late meal ordering
- [ ] Token system
- [ ] Login / log out
- [ ] Register a new user
- [ ] Homepage with portals
- [ ] My profile (SDRs + turn room sharing on/off)
- [ ] Password reset
- [ ] Get rid of active tokens daily
- [ ] Sport portal and ask for sport
- [ ] Coffee Night portal and ask for coffee night + permissions
- [ ] Remove outdated semester response code
- [ ] Update 'what can you do?'
- [ ] Send a message to officers every time there's a 500

### Refactor

- [ ] Split into files grouping functionality
- [ ] Continue finding bugs in refactored code
- [ ] Move functions from functions.py into their new files
- [ ] Fix hashbrowns
- [ ] Fix J&D
- [ ] Fix the update and loveorla routes
- [ ] Look at the sonnet code
- [ ] Pydoc for all functions
- [ ] Make sure functions are modularised so tests can be written
- [ ] Fix error raising and handling to work properly/standardised

### Testing / Continuous Integration Framework

- [ ] Figure out how to setup a local db to run tests on
- [ ] Figure out how to get pytest to work with the folders
- [ ] Setup CI & runner to run tests every time dev/master is pushed to (+pylint)
- [ ] Write comprehensive tests for all functions

### Functionality - Future

- [ ] Blast notifications
- [ ] Get Dino times
- [ ] Vactrack
- [ ] Finish 'I want to go home'
- [ ] Reverse room number - get name by room number (if allowed)

# Todo - 2019

## 1.0.0 (Release)
- [x] dino menus
- [x] dino polls
	- [x] Facebook quick replies
- [x] duty tutor
- [x] j and d on
	- [x] J&D location system
- [x] maintain database of users / PSID / last use
	- [x] send blast notifications to active users
- [x] split up code so it's less spaghetti 🍝 (It's still spaghett)

#### Administrative

- [x] Submit for facebook review
- [x] Get business documentation from Joel
- [ ] Github -> heroku system so other people can work on it
- [x] Donate to Ops and Comms??

## 1.1.0
- [x] convert to pipenv rather than requirements.txt
- [x] What can you do?
- [x] Dinovote
	- [x] Basic functionality
	- [ ] send poll 30 minutes after message sent
		- [ ] Option to unsubscribe
	- [ ] If someone has voted, put it in the "what's dino" message after menu
- [ ] Ensure that blast notifications conform to 24 + 1 facebook rule
- [ ] Add login / password system for backend
- [ ] Nice interface for backend
- [ ] Edit meals in backend
- [ ] Ordered meals in backend
- [ ] Auto delete meals after a particular date
- [ ] General Knowledge base (https://github.com/jajoosam/wikibot/blob/master/server.js)
- [x] Room number database
- [x] Ability to ask for day of the week's dinner (i.e what is for dinner on wednesday)
- [x] other events
	- [x] show calendar image?
- [x] Show "no one has voted for *dinner* at dino" to be clear
- [x] setshop on --> "shopen? / is shop open?"
- [x] Semester Progress Bar
- [ ] Coffee night recap
#### Meta:

- [x] create program to test on local machine by sending curl requests to webhook on server [see ngrok]
	- [ ] dev heroku app??
- [ ] create way to autogen next week's meals for testing
- [ ] put functions into modules to clean up code


## 1.2.0
- [ ] Socials
	- [ ] When / Where is bus leaving?
	- [ ] setbus 16:00 <-- same as setjd on for bus times (then "Bus time?")
	- [ ] Group distribution automation in backend (for date nights etc)
	- [ ] Use subscription messaging to be notified about bus times etc: https://developers.facebook.com/docs/messenger-platform/policy/policy-overview/#subscription_messaging
- [ ] Welcome screen (personalised greeting)
- [ ] Better error handling
- [ ] let xanthe know I can't come to coffee night
	- [ ] Send email to Xanthe with user created excuse
- [ ] Send feature request through BaxtaBot
- [ ] Send Typing bubbles


## The Future

- [ ] Vactrac integration
- [ ] Knowledge graphs (cc Zac Moran)
- [ ] Actual NLP
- [ ] Shaqquotes ("Change is the only constant")
- [ ] Buy tickets to things through baxtabot
	- see https://developers.facebook.com/docs/messenger-platform/send-messages/template/receipt
- [ ] Object recognition in shop -> gives price
- [ ] Rig up raspberry pi to ping baxtabot.herokuapp.com every 30 minutes to ensure heroku does not fall asleep
- [ ] Potentially an authentication system ... store if PSID knows the password???

## Social Features
- [ ] Pub crawls -> Down your drink random
- [ ] TKC Dating "find me a lover"
	- [ ] Allow floorcest?
