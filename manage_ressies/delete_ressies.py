import csv
import urllib.request
import json
import ssl

x = 78
while True:
    try:
        request = urllib.request.Request(f'https://baxtabot.herokuapp.com/ressie/delete/{x}')

        gcontext = ssl.SSLContext()
        response = urllib.request.urlopen(request, context=gcontext)
        payload = response.read().decode('utf8')
        print(x)
        x += 1
    except:
        print(x)
        break
