"""
Author: Jeff Levensailor
Email: jeff@levensailor.com
https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cuipph/all_models/xsi/9-1-1/CUIP_BK_P82B3B16_00_phones-services-application-development-notes.html
"""

import logging
import requests
from requests.auth import HTTPBasicAuth
import time

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

def enter():
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3ANavSelect%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def up():
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3ANavUp%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def down():
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3ANavDwn%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def left():
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3ANavLeft%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"

def right():
    return "XML=%3CCiscoIPPhoneExecute%3E%3CExecuteItem%20URL%3D%22Key%3ANavRight%22%2F%3E%3C%2FCiscoIPPhoneExecute%3E"


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


def alt_tftp_7960(phone):
    remoteCTI(phone,settings())
    remoteCTI(phone,keypad('3'))
    for i in range(0,32):
        remoteCTI(phone,down())
    remoteCTI(phone,keypad('*'))
    remoteCTI(phone,keypad('*'))
    remoteCTI(phone,keypad('#'))
    remoteCTI(phone,softkey('2'))
    remoteCTI(phone,softkey('3'))
    remoteCTI(phone,keypad('*'))
    remoteCTI(phone,keypad('*'))
    remoteCTI(phone,keypad('#'))
    remoteCTI(phone,softkey('2'))
    remoteCTI(phone,softkey('3'))
'''
Macros per model to wipe out ITL files
'''
def macro7970(phone):
    remoteCTI(phone,settings())
    remoteCTI(phone,keypad('4'))
    remoteCTI(phone,keypad('5'))
    remoteCTI(phone,keypad('2'))
    remoteCTI(phone,softkey('5'))

def macro7900(phone):
    remoteCTI(phone,settings())
    remoteCTI(phone,keypad('4'))
    remoteCTI(phone,keypad('5'))
    remoteCTI(phone,keypad('2'))
    remoteCTI(phone,star())
    remoteCTI(phone,star())
    remoteCTI(phone,pound())
    remoteCTI(phone,softkey('2'))
    remoteCTI(phone,softkey('4'))
    remoteCTI(phone,softkey('2'))

def macro8800(phone):
    remoteCTI(phone,applications())
    remoteCTI(phone,keypad('5'))
    remoteCTI(phone,keypad('4'))
    remoteCTI(phone,keypad('2'))
    remoteCTI(phone,softkey('3'))




def reset_itl(phone):
    model = phone['model']
    ip = phone['ip']
    if model.startswith('Cisco IP Phone 796') and not model.endswith('0') and ip:
        macro7900(ip)
    elif model.startswith('Cisco IP Phone 794') and not model.endswith('0') and ip:
        macro7900(ip)
    elif model.startswith('Cisco IP Phone 797') and not model.endswith('0') and ip:
        macro7970(ip)
    elif model.startswith('Cisco IP Phone 88') and ip:
        macro8800(ip)
    else:
        return 'Macro for phone not found'

phone = {}
phone['model'] = 'Cisco IP Phone 8851'
phone['ip'] = '10.131.202.127'

# reset_itl(phone)

alt_tftp_7960('10.47.11.175')