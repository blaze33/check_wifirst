# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import requests
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
            payload[input['name']] = input['value']
    if hasattr(parser, 'form'):
        for x, y in parser.form:
            if x == 'action':
                form_action = y
    return payload, form_action


login = 'rouyrrem'
with open('password.txt') as f:
    password = f.readline().split()[0]

url = 'https://selfcare.wifirst.net/sessions/new'
user_agent = "Mozilla/5.0"
r = requests.get(url)
r.headers['User-Agent'] = user_agent
print "#### request 1: get"
print r.status_code
cookies = r.cookies
print "Cookie: ", cookies
payload, url = scrap_form(r.content)

payload['remember_me'] = '1'
payload['login'] = login
payload['password'] = password
payload['commit'] = 'Se connecter'

h = {
    'Content-Length': len(unicode(payload)),
    'User-Agent': user_agent,
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    # 'Accept-Encoding': 'gzip,deflate,sdch',
    # 'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
    # 'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'Content-Type': 'application/x-www-form-urlencoded',
    # 'Host': 'selfcare.wifirst.net',
    'Origin': 'https://selfcare.wifirst.net',
    # 'Referer': 'https://selfcare.wifirst.net/sessions',
}

print "#### request 2: post login pwd"
# print url, h, payload, "length: ", len(unicode(payload))
r = requests.post('https://selfcare.wifirst.net/sessions',
                  headers=h, data=payload, cookies=cookies)
print r.url, r.status_code, len(r.content)
# print "\nresponse: headers: ", r.headers
cookies = r.cookies
print "Cookie: ", cookies
if len(r.content) < 200:
    print ' * content: ', r.content

print "#### request 3: get perform"
r = requests.get('https://connect.wifirst.net/?perform=true', cookies=cookies)
print r.url, r.headers['status']
payload, url = scrap_form(r.content)
payload['remember_me'] = '1'

print "#### request 4: final post to connect"
print payload
print url
r = requests.post(url, data=payload, cookies=cookies)
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
