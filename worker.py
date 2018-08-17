# Worker.py
#
# Deals with all blocking tasks such as dinoPollCheck
# could also do some other shit with redis queuing for heftier functions see:
# https://devcenter.heroku.com/articles/python-rq

# import schedule
# import time
#
# schedule.every(15).minutes.do(functions.dino.dinoPollCheck())
#
# if __name__ == '__main__':
#     while True:
# 	    schedule.run_pending()
# 	    time.sleep(1)
