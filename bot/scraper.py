# -*- coding: utf-8 -*-

__author__ = 'bardia'

url = "https://stu.iust.ac.ir/loginpage.rose"
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import re


def encoded_dict(in_dict):
    out_dict = {}
    for k, v in in_dict.iteritems():
        if isinstance(v, unicode):
            v = v.encode('utf8')
        elif isinstance(v, str):
            # Must be encoded in UTF-8
            v.decode('utf8')
        out_dict[k] = v
    return out_dict


def check((username, password)):
    # Store the cookies and create an opener that will hold them
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    # Add our headers
    opener.addheaders = [('User-agent', 'RedditTesting')]

    # Install our opener (note that this changes the global opener to the one
    # we just made, but you can also just call opener.open() if you want)
    urllib2.install_opener(opener)

    # The action/ target from the form
    authentication_url = "https://stu.iust.ac.ir/j_security_check"

    # Input parameters we are going to send
    payload = encoded_dict({"j_username": username,
                            "j_password": password,
                            "login": u"ورود", })

    # Use urllib to encode the payload
    data = urllib.urlencode(payload)

    # Build our Request object (supplying 'data' makes it a POST)
    req = urllib2.Request(authentication_url, data)

    # Make the request and read the response
    resp = urllib2.urlopen(req)
    contents = resp.read()

    if contents.find('iconWarning.gif') != -1:
        #print contents
        return False, None, None

    soup = BeautifulSoup(contents)
    user_info = soup.body.table.tr.find_all('td')[4].div.contents[0].replace(u'\xA0', ' ').replace('\n', ' ').encode(
        'utf8')
    matches = re.findall(r"\d{8}", user_info)
    if len(matches) != 0:
        return False, None, None
    uni_id = matches[0]
    name = str(user_info).replace(uni_id, "").replace(u'\xA0', ' ').strip()
    if len(name) < 3:
        return False, None, None
    return True, name, uni_id


def credit((username, password)):
    # Store the cookies and create an opener that will hold them
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    # Add our headers
    opener.addheaders = [('User-agent', 'RedditTesting')]

    # Install our opener (note that this changes the global opener to the one
    # we just made, but you can also just call opener.open() if you want)
    urllib2.install_opener(opener)

    # The action/ target from the form
    authentication_url = "https://stu.iust.ac.ir/j_security_check"

    # Input parameters we are going to send
    payload = encoded_dict({"j_username": username,
                            "j_password": password,
                            "login": u"ورود", })

    # Use urllib to encode the payload
    data = urllib.urlencode(payload)

    # Build our Request object (supplying 'data' makes it a POST)
    req = urllib2.Request(authentication_url, data)

    # Make the request and read the response
    resp = urllib2.urlopen(req)
    contents = resp.read()

    if contents.find('iconWarning.gif') != -1:
        print "error"
        return False
    #

    credit_url = "https://stu.iust.ac.ir/nurture/user/credit/charge/view.rose"

    req = urllib2.Request(credit_url, data)

    # Make the request and read the response
    resp = urllib2.urlopen(req)
    contents = resp.read()
    soup = BeautifulSoup(contents)
    user_credit = re.findall(r"\d+",
                             soup.find(id="charge").find_all("table")[2].tr.td.table.tr.find_all('td')[1].contents[
                                 0].replace(u'\xA0', ' ').replace('\n', ' ').strip())[0]
    print 'credit:', user_credit
    return int(user_credit)


if __name__ == "__main__":
    print credit(("92521114", "0017578167"))
    # print check(("92521114", "0017578167"))