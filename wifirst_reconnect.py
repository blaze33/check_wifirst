# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import requests
from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    inputs=[]

    def handle_starttag(self, tag, attrs):
        if tag=='input':
            self.inputs.append(dict(attrs))
        if tag=='form':
            self.form = attrs
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        pass

def scrap_form(content):# instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed(content)

    payload = {}

    for input in parser.inputs:
        if input['type'] != 'submit':
            payload[input['name']] = input['value']
    for x, y in parser.form:
        if x=='action':
            form_action = y
    return payload, form_action

login = 'rouyrrem'
with open('password.txt') as f:
    password = f.readline().split()[0]

url = 'https://selfcare.wifirst.net/sessions/new'

r = requests.get(url)
print r.url, r.headers['status']
cookies = r.cookies
payload, url = scrap_form(r.content)

payload['remember_me'] = '1'
payload['login'] = login
payload['password'] = password

r = requests.post('https://selfcare.wifirst.net/sessions/', data=payload, cookies=cookies)
print r.url, r.headers['status']
r = requests.get('https://connect.wifirst.net/?perform=true', cookies=cookies)
print r.url, r.headers['status']
payload, url = scrap_form(r.content)
payload['remember_me'] = '1'
r = requests.post(url, data=payload, cookies=cookies)
print r.url, r.headers['status']

# <codecell>


# <codecell>


