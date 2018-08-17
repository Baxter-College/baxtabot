# environment.py
#
# Get all environment variables

import os

if 'HEROKU' in os.environ:
	DEBUG = int(os.environ.get('DEBUG'))
	PORT = int(os.environ.get('PORT'))
	PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
else:
	DEBUG = 1
	PORT = 5000
	PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']


print("access token is: ", PAGE_ACCESS_TOKEN)
VERIFY_TOKEN = "GoodLordyThomasJHillLooksFineTonight"
