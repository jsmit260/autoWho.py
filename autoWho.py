import pycurl
import io
import sys
import json
import re
import os, sys
import time
import requests
import string
 
buffer = io.StringIO()


#1 Create a pycurl.Curl instance

try:
    uri = ('https://ipinfo.io/'+sys.argv[1])
except IndexError:
    print('NO IP GIVEN -- USAGE:> autoWho.py 8.8.8.8')
    sys.exit()


#SANTIZE RFC1918 and abnormal IP entries
if re.match(r'^((([2][5][0-5]|([2][0-4]|[1][0-9]|[0-9])?[0-9])\.){3})([2][5][0-5]|([2][0-4]|[1][0-9]|[0-9])?[0-9])$',sys.argv[1]) is None:
                sys.exit("Invalid IPv4 format")

if re.match(r'^(((25[0-5]|2[0-4][0-9]|19[0-1]|19[3-9]|18[0-9]|17[0-1]|17[3-9]|1[0-6][0-9]|1[1-9]|[2-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9]))|(192\.(25[0-5]|2[0-4][0-9]|16[0-7]|169|1[0-5][0-9]|1[7-9][0-9]|[1-9][0-9]|[0-9]))|(172\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|1[0-5]|3[2-9]|[4-9][0-9]|[0-9])))\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$',sys.argv[1]) is None:
                sys.exit("You can not use WHOIS on RFC1918 addresses. Please enter a public IP address. :) ")



def api_call():
    s = requests.Session()
    headers ={}
    data = {}
    targeturl = 'https://ipinfo.io/'
    r = s.get(str(uri))
    return r

data = api_call().json()
print('\n'+ 'IP address ' + data['ip'] + ' belongs to ' + data['org'] + ' out of ' + data['country'] + ', ' +data['region'] +'\n')
