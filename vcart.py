#!/usr/bin/python

import sys
import re
import json
import urllib
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup

username = raw_input("Username: ")
password = raw_input("Password: ")

login_url = "https://www.vinmonopolet.no/vmpSite/j_spring_security_check"
add_url = "https://www.vinmonopolet.no/vmpSite/cart/add"
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

def get_token(url, t_type):
    try:
        r = opener.open(url)
    except urllib2.HTTPError, error:
        print error.read()
    html = BeautifulSoup(r.read())
    if t_type == "add":
        csrf_token = html.find('form', {'id': 'add_to_cart_storepickup_form'}).find('input', {'name': 'CSRFToken'}).get('value')
    if t_type == "login":
        csrf_token = html.find('form', {'id': 'js-login-form'}).find('input', {'name': 'CSRFToken'}).get('value')
    return csrf_token

def add_to_cart(item):
    item_url = urllib2.urlopen('https://www.vinmonopolet.no/vmpSite/search/autocomplete/SearchBox?term=' + item)
    item_url = 'https://www.vinmonopolet.no/' + json.loads(item_url.read())["products"][0]["url"]
    csrf_token = get_token(item_url, "add")
    data = urllib.urlencode({'productCodePost': item,
                            'qty': '1',
                            'CSRFToken' : csrf_token})
    try:
        r = opener.open(add_url, data)
    except urllib2.HTTPError, error:
        print error.read()
    print "Added item: " + item

def login_polet(uname, pword):
    csrf_token = get_token("https://www.vinmonopolet.no/vmpSite/login", "login")
    login_data = urllib.urlencode({
        'j_username': uname,
        'j_password': pword,
        'CSRFToken': csrf_token})
    try:    
        r = opener.open(login_url, login_data)
    except urllib2.HTTPError, error:
        print error.read()

def main():
    item_file = sys.argv[1]

    login_polet(username, password)

    f = open(item_file, 'r')
    for i in f.readlines():
        add_to_cart(i.rstrip())
    f.close()

if __name__ == "__main__":
    main()
