import sys
import re
import PySimpleGUI as sg
from datetime import datetime
import pytz


def get_device():
    """
    Prompts the user with a form in which he must
    specify the IP address of the device he wants to configure
    """
    title = 'Enter the IP address of the device'

    layout = [
        [sg.T('IP address')],
        [sg.In(size=(30, 1), key='host')],
        [sg.OK(size=(15, 1)), sg.Cancel(size=(15, 1))]
    ]

    window = sg.Window(title, layout)

    while True:
        event, values = window.Read()
        if event in [None, 'Cancel']:
            sys.exit()
        else:
            if re.match(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]'
                        r'[0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]'
                        r'|[01]?[0-9][0-9]?)$', values['host']):
                break
            else:
                sg.Popup('Invalid IP')

    return values['host']


def get_credentials(host):
    """
    Prompts the user with a login form and returns a tuple
    containing (username, password, secret).
    """
    title = f'{host} - Login Information'

    layout = [
        [sg.T('Username'), sg.In(size=(30, 1), key='username')],
        [sg.T('Password'), sg.In(size=(30, 1), key='password', password_char='*')],
        [sg.T('Secret'), sg.In(size=(30, 1), key='secret', password_char='*')],
        [sg.T(''), sg.OK(size=(10, 1)), sg.Cancel(size=(10, 1))]

    ]

    window = sg.Window(title, auto_size_text=False, default_element_size=(10,1),
                       text_justification='r',
                       grab_anywhere=False).Layout(layout)

    event, values = window.read()
    if event in [None, 'Cancel']:
        sys.exit()

    return values['username'], values['password'], values['secret']


def form_secure_login(host, current_clock, hostname):
    """
    Prompts the user with a form for configuring
    a Cisco device for secure login.
    """
    title = f'{host} - Secure Login Configuration'
    timezones = ('UTC-12', 'UTC-11', 'UTC-10', 'UTC-9', 'UTC-8', 'UTC-7', 'UTC-6',
                 'UTC-5', 'UTC-4', 'UTC-3', 'UTC-2', 'UTC-1', 'UTC+0', 'UTC+1',
                 'UTC+2', 'UTC+3', 'UTC+4', 'UTC+5', 'UTC+6', 'UTC+7', 'UTC+8',
                 'UTC+9', 'UTC+10', 'UTC+11', 'UTC+12', 'UTC+13', 'UTC+14')

    layout = [
        [sg.Frame(layout=[
            [sg.T('Device time:', size=(12, 1)),
             sg.T(f'{current_clock}')],
            [sg.T('Current time:', size=(12, 1)),
             sg.T(f"{pytz.utc.localize(datetime.utcnow()).strftime('%H:%M:%S %Z %a %b %d %Y')}")],
            [sg.Radio('Keep device time', 'RADIO1', default=True, size=(15, 1), key='keep_time'),
             sg.Radio('Update time to current time', 'RADIO1', key='update_time')],
            [sg.T('Select your regional timezone'),
             sg.InputCombo(timezones, key='timezone', default_value=timezones[15])]
            ], title='Time settings')],
        [sg.T('Device hostname', size=(12, 1)),
         sg.In(size=(15, 1), default_text=f'{hostname}', key='hostname')],
        [sg.Frame(layout=[
            [sg.T('Username', size=(15, 1)), sg.In(size=(15, 1), default_text='admin', key='username')],
            [sg.T('Password', size=(15, 1)), sg.In(size=(15, 1), password_char='*', key='password')],
            [sg.T('Confirm Password', size=(15, 1)), sg.In(size=(15, 1), password_char='*', key='password_confirm')],
        ], title='Create new username')],
        # TODO:
        #  Line vty 0 4
        # 	Exec-timeout <minutes> <secs>
        # 	Login local
        # 	Transport input ssh
        # 	Exit
        #  Line console 0
        # 	Exec-timeout <minutes> <secs>
        # 	Login local
        # 	Exit
        #  Banner login /Insert text here./
        #  Login block-for <secs> attempts <tries> within <secs>
        #  Ip access-list standard <nume acl>
        # 	Remark Permite accesul doar hosturilor de administrare
        # 	Permit <IP> <wildcard>
        # 	Permit <IP> <wildcard>
        # 	exit
        #  Login quiet-mode access-class <acl-name/acl-number>
        #  Login delay <secs>
        #  Login on-success log
        #  Login on-failure log
        #  !ENABLE SSH
        #  Ip domain-name <domain>
        #  Crypto key generate rsa general-keys modulus 2048
        #  Ip ssh version 2
        #  Ip ssh time-out <secs>
        #  Ip ssh authentication-retries <number of retries>

        [sg.OK()]
    ]

    window = sg.Window(title, layout)

    event, values = window.Read()

    return event, values