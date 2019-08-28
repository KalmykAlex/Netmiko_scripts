import sys
import re
import PySimpleGUI as sg


def select_device():
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
