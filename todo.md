# Todo


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
- [ ] Dinovote
	- [ ] send poll 30 minutes after message sent
	- [ ] If someone has voted, put it in the "what's dino" message after menu
- [ ] Ensure that blast notifications conform to 24 + 1 facebook rule
- [ ] Send Typing bubbles
- [ ] Add login / password system for backend
- [ ] Nice interface for backend
- [ ] Edit meals in backend
- [ ] Ordered meals in backend
- [ ] Auto delete meals after a particular date
- [x] Ability to ask for day of the week's dinner (i.e what is for dinner on wednesday)
- [x] other events
	- [x] show calendar image?
- [ ] let xanthe know I can't come to coffee night
	- [ ] Send email to Xanthe with user created excuse
- [ ] Send feature request through BaxtaBot
- [ ] Show "no one has voted for *dinner* at dino" to be clear
- [ ] setshop on --> "shopen? / is shop open?"

#### Meta:

- [x] create program to test on local machine by sending curl requests to webhook on server [see ngrok]
- [ ] create way to autogen next week's meals for testing


## 1.2.0
- [ ] Socials
	- [ ] When / Where is bus leaving?
	- [ ] setbus 16:00 <-- same as setjd on for bus times (then "Bus time?")
	- [ ] Group distribution automation in backend (for date nights etc)
- [ ] Potentially an authentication system ... store if PSID knows the password???
- [ ] Calendars (.ics)
	- [ ] Individual calendar upload (see https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python)
	- [ ] Baxter Event calendars
- [ ] Semester Progress Bar
- [ ] Use subscription messaging to be notified about bus times etc: https://developers.facebook.com/docs/messenger-platform/policy/policy-overview/#subscription_messaging
- [ ] Welcome screen (personalised greeting)
- [ ] Better error handling


## The Future

- [ ] Vactrac integration
- [ ] Knowledge graphs (cc Zac Moran)
- [ ] Actual NLP
- [ ] Shaqquotes ("Change is the only constant")
- [ ] Buy tickets to things through baxtabot
	- see https://developers.facebook.com/docs/messenger-platform/send-messages/template/receipt
- [ ] Object recognition in shop -> gives price
- [ ] Rig up raspberry pi to ping baxtabot.herokuapp.com every 30 minutes to ensure heroku does not fall asleep
