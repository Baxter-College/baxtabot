import csv
import urllib.request
import json
import ssl

x = 219
while True:
    try:
        request = urllib.request.Request(f'https://baxtabot.herokuapp.com/ressie/delete/{x}')

        gcontext = ssl.SSLContext()
        response = urllib.request.urlopen(request, context=gcontext)
        payload = response.read().decode('utf8')
        print('Success:', x)
        x += 1
    except Exception as e:
        print('Something went wrong', x, e)
        break
