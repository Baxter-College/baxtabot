import csv
import urllib.request
import urllib.parse
import json
import ssl

with open('T3 Baxter.csv') as FILE:
    reader = csv.reader(FILE)
    next(reader, None)

    for row in reader:
        last_name, first_name, room_number = row
        last_name = last_name.capitalize()
        last_name_edited = ''
        for char in last_name:
            if char == '(' or char == ' ':
                break
            else:
                last_name_edited += char

        entry = urllib.parse.urlencode({'last_name':last_name_edited,
                'first_name':first_name,
                'room_number':room_number[:3]}).encode()
        print(first_name, last_name_edited, room_number)
        request = urllib.request.Request('https://baxtabot.herokuapp.com/ressie', data=entry)

        gcontext = ssl.SSLContext()
        response = urllib.request.urlopen(request, context=gcontext)
        payload = response.read().decode('utf8')
