import sys
import PySimpleGUI as sg

def get_credentials(device_name):
    """
    Prompts the user with a login form and returns a tuple
    containing (username, password, secret).
    """
    title = f'{device_name} - Login Information'

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