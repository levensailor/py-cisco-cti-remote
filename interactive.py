"""
Author: Jeff Levensailor
Email: jeff@levensailor.com
https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cuipph/all_models/xsi/9-1-1/CUIP_BK_P82B3B16_00_phones-services-application-development-notes.html
"""

import requests
from requests.auth import HTTPBasicAuth
import readline
import shlex
import logging
import time
import ipaddress

logging.basicConfig(
format='%(asctime)s %(levelname)s: %(message)s',
datefmt='%m/%d/%Y %I:%M:%S %p', 
level=logging.INFO
)

cti_user = 'ctiuser'
cti_pass = 'ctipassword'

def keypad(num):
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3AKeyPad"+num+"%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def softkey(num):
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3ASoft"+num+"%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def star():
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3AKeyPadStar%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def pound():
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3AKeyPadPound%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def settings():
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3ASettings%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def applications():
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3AApplications%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def parse(response):
    if response == '<CiscoIPPhoneError Number="1" />':
        logging.info('Error parsing CiscoIPPhoneExecute object')
    elif response == '<CiscoIPPhoneError Number="2" />':
        logging.info('Error framing CiscoIPPhoneResponse object')
    elif response == '<CiscoIPPhoneError Number="3" />':
        logging.info('Internal file error')
    elif response == '<CiscoIPPhoneError Number="4" />':
        logging.info('Authentication Error')
    elif 'Success' in response:
        logging.info('OK')
    else:
        logging.info(response)

def remoteCTI(phone, payload):
    url = "http://"+phone+"/CGI/Execute"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    try:
        response = requests.request("POST", url, auth=HTTPBasicAuth(cti_user, cti_pass), data=payload, headers=headers)
        parse(response.text)
    except requests.exceptions.RequestException as e:
        logging.info(e)
    time.sleep(1)

def promptForIP():
    try:
        phone = input('Enter your phone ip address: ')
        if ipaddress.ip_address(phone):
            return phone
    except ValueError as e:
        logging.info(e)
        promptForIP()

phone = promptForIP()
print('Enter a key to press, or type help')

while True:
    cmd, *args = shlex.split(input('> '))

    if cmd.isdigit():
        remoteCTI(phone, keypad(cmd))

    elif cmd=='*':
        remoteCTI(phone, star())

    elif cmd=='#':
        remoteCTI(phone, pound())

    elif len(cmd)==2 and cmd[:1] == 's' and cmd[1:].isdigit():
        remoteCTI(phone, softkey(cmd[1:]))

    elif cmd=='s' or cmd=='S':
        remoteCTI(phone, settings())

    elif cmd=='a' or cmd=='A':
        remoteCTI(phone, applications())

    elif cmd=='exit':
        exit()

    elif cmd=='help':
        print('============================================')
        print('Type the key you wish to press, one at a time')
        print('0-9, # and * will press the respective digit')
        print('for Softkeys, prepend with s.. ie: s1 for Softkey 1')
        print('for Settings, type s - Applications, type a')
        print('============================================\n')

    else:
        print('Unknown command: {}'.format(cmd))