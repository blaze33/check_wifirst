# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import requests
import pprint
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):
# create a subclass and override the handler methods
    inputs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            self.inputs.append(dict(attrs))
        if tag == 'form':
            self.form = attrs

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


def scrap_form(content):  # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed(content)

    payload, form_action = {}, ''

    for input in parser.inputs:
        if input['type'] != 'submit':
            payload[input['name']] = input.get('value')
    if hasattr(parser, 'form'):
        for x, y in parser.form:
            if x == 'action':
                form_action = y
    return payload, form_action


login = 'rouyrrem'
with open('password.txt') as f:
    password = f.readline().split()[0]

url = 'https://selfcare.wifirst.net/sessions/new'
s = requests.Session()
r = s.get(url)

print "#### request 1: get"
print r.url, r.status_code, len(r.content)
payload, url = scrap_form(r.content)
payload.update({
    'remember_me': '1',
    'login': login,
    'password': password,
    'commit': 'Se connecter'
})

print "\n#### request 2: post login pwd"
r = s.post('https://selfcare.wifirst.net/sessions', data=payload)
print r.url, r.status_code, len(r.content)
# print "\nresponse: headers: ", r.headers
if len(r.content) < 200:
    print ' * content: ', r.content

print "\n#### request 3: get perform"
r = s.get('https://connect.wifirst.net/?perform=true')
print r.url, r.headers['status']
payload, url = scrap_form(r.content)
payload['remember_me'] = '1'

print "\n#### request 4: final post to connect"
# pprint.pprint(payload)
print url
r = s.post(url, data=payload)
print r.url, r.headers['status']

success = True
from subprocess import call
return_code = call("ping -q -w 1 -c 1 google.com", shell=True)
if return_code == 0:
    message = "Success."
else:
    message = "Failed. Ping return code: {}".format(return_code)

import datetime
import pytz
time = datetime.datetime.now(
    pytz.timezone('Europe/Paris')).strftime('%d/%m/%Y:%H:%M:%S %z')
with open("reconnections.log", "a") as myfile:
    myfile.write("[{}] {}\n".format(time, message))
