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


def get_device_type():
    """
    Prompts the user with a form in which to chose
    the device type from a predefined list
    """
    DEVICE_TYPES = ['cisco_ios', 'cisco_asa']

    title = 'Select device type'

    layout = [
        [sg.Radio('Cisco IOS', 'RADIO2', default=True, size=(15, 1), key='ios')],
        [sg.Radio('Cisco ASA', 'RADIO2', size=(15, 1), key='asa')],
        [sg.OK(size=(10, 1)), sg.Cancel(size=(10, 1))]
    ]

    window = sg.Window(title, layout)

    while True:
        event, values = window.Read()
        if event in [None, 'Cancel']:
            sys.exit()
        else:
            if values['ios'] == True:
                return DEVICE_TYPES[0]
            elif values['asa'] == True:
                return DEVICE_TYPES[1]



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

    while True:
        event, values = window.read()
        if event in [None, 'Cancel']:
            sys.exit()
        elif '' in values.values():
            sg.Popup('Empty field')
        else:
            break

    return values['username'], values['password'], values['secret']


def form_secure_login(host, current_clock, hostname, domain, users):
    """
    Prompts the user with a form for configuring
    a Cisco device for secure login.
    """
    title = f'{host} - Secure Login Configuration'
    timezones = ('UTC-12', 'UTC-11', 'UTC-10', 'UTC-9', 'UTC-8', 'UTC-7', 'UTC-6',
                 'UTC-5', 'UTC-4', 'UTC-3', 'UTC-2', 'UTC-1', 'UTC+0', 'UTC+1',
                 'UTC+2', 'UTC+3', 'UTC+4', 'UTC+5', 'UTC+6', 'UTC+7', 'UTC+8',
                 'UTC+9', 'UTC+10', 'UTC+11', 'UTC+12', 'UTC+13', 'UTC+14')
    spinbox_minutes = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                       '11', '12', '13', '14', '15', '16', '17', '18', '19', '20')
    spinbox_seconds = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                       '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                       '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                       '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
                       '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
                       '51', '52', '53', '54', '55', '56', '57', '58', '59')
    spinbox_delay = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')

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
        [sg.T('Domain', size=(12, 1)),
         sg.In(size=(15, 1), default_text=f'{domain}', key='domain')],
        [sg.T(f'Configured users: {str(users).replace("[","").replace("]","")}',)],
        [sg.Frame(layout=[
            [sg.T('Username', size=(15, 1)),
             sg.In(size=(15, 1), default_text='admin', key='username')],
            [sg.T('Password', size=(15, 1)),
             sg.In(size=(15, 1), password_char='*', key='password')],
            [sg.T('Confirm Password', size=(15, 1)),
             sg.In(size=(15, 1), password_char='*', key='password_confirm')],
        ], title='Create new username')],
        [sg.T('SSH exec timeout', size=(17, 1)),
         sg.T('minutes'),
         sg.Spin(values=spinbox_minutes, initial_value='3', size=(2, 1), key='ssh_timeout_min'),
         sg.T('seconds'),
         sg.Spin(values=spinbox_seconds, initial_value='0', size=(2, 1), key='ssh_timeout_sec')],
        [sg.T('Console exec timeout', size=(17, 1)),
         sg.T('minutes'),
         sg.Spin(values=spinbox_minutes, initial_value='3', size=(2, 1), key='con_timeout_min'),
         sg.T('seconds'),
         sg.Spin(values=spinbox_seconds, initial_value='0', size=(2, 1), key='con_timeout_sec')],
        [sg.T('Banner')],
        [sg.Multiline(size=(35, 3), key='banner', default_text='/Default Banner/')],
        [sg.Frame(layout=[
            [sg.T('ACL Name', size=(8, 1)), sg.In(size=(20, 1), key='acl_name')],
            [sg.T('Remark', size=(8, 1)), sg.In(size=(20, 2), key='acl_remark')],
            [sg.T('Permit', size=(8, 1)),
             sg.T('IP'), sg.In(size=(15, 1), key='ip'),
             sg.T('Wildcard'), sg.In(size=(15, 1), key='wildcard')],
        ], title='Access Control')],
        [sg.T('Delay between successive fail login'),
         sg.Spin(values=spinbox_delay, initial_value='3', size=(2, 1), key='login_delay')],
        [sg.Checkbox('Log successful logins', key='log_success_login')],
        [sg.Checkbox('Log failed logins', key='log_failure_login')],
        [sg.OK()]
    ]

    #TODO: user input validation

    window = sg.Window(title, layout)

    event, values = window.Read()

    return event, values


def progress_bar(host):
    """Displays a progress bar that informs the user on the currently running processes."""

    title = f'Fetching device information from {host}'
    layout = [
        [sg.ProgressBar(1, orientation='h', size=(40, 10), key='progress')]
    ]
    window = sg.Window(title, layout, auto_size_text=False, default_element_size=(10,1)).Finalize()
    progress = window.FindElement('progress')

    return progress
