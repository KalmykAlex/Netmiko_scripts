import sys
import re
import PySimpleGUI as sg
from datetime import datetime
import pytz


class UserInterface:

    @staticmethod
    def get_device_window():
        """
        Prompts the user with a form in which he must
        specify the IP address of the device he wants to configure
        """
        title = 'Enter the IP address of the device'

        layout = [
            [sg.T('IP address', size=(20, 1))],
            [sg.In(size=(25, 1), key='host')],
            [sg.OK(size=(10, 1)), sg.Cancel(size=(10, 1))]
        ]

        window = sg.Window(title, layout, element_justification='center')

        while True:
            event, values = window.Read()
            if event in [None, 'Cancel']:
                sys.exit()
            else:
                if re.match(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]'
                            r'[0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]'
                            r'|[01]?[0-9][0-9]?)$', values['host']):
                    window.Close()
                    break
                else:
                    sg.Popup('Invalid IP')

        return values['host']

    @staticmethod
    def get_device_type_window():
        """
        Prompts the user with a form in which to chose
        the device type from a predefined list
        """
        DEVICE_TYPES = ['cisco_ios', 'cisco_asa']

        title = 'Select device type'

        layout = [
            [sg.Radio('Cisco IOS', 'RADIO2', default=True, key='ios')],
            [sg.Radio('Cisco ASA', 'RADIO2', key='asa')],
            [sg.OK(size=(10, 1)), sg.Cancel(size=(10, 1))]
        ]

        window = sg.Window(title, layout, element_justification='left')

        while True:
            event, values = window.Read()
            if event in [None, 'Cancel']:
                sys.exit()
            else:
                if values['ios'] == True:
                    window.Close()
                    return DEVICE_TYPES[0]
                elif values['asa'] == True:
                    window.Close()
                    return DEVICE_TYPES[1]

    @staticmethod
    def get_credentials_window(host):
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
                           text_justification='right',
                           grab_anywhere=False).Layout(layout)

        while True:
            event, values = window.Read()
            if event in [None, 'Cancel']:
                sys.exit()
            elif '' in values.values():
                sg.Popup('Empty field')
            else:
                window.Close()
                break

        return values['username'], values['password'], values['secret']

    @staticmethod
    def add_user_window(host, logged_on_priv):
        """Prompts the user with a form for adding a new user."""
        title = f'Add a new user to {host}'

        layout = [
            [sg.T('Username'), sg.In(size=(30, 1), key='username')],
            [sg.T('Password'), sg.In(size=(30, 1), key='password_1', password_char='*')],
            [sg.T('Verify Password'), sg.In(size=(30, 1), key='password_2', password_char='*')],
            [sg.T('Privilege Level'),
             sg.Spin(values=[i for i in range(logged_on_priv+1)],
                     initial_value='0', size=(2, 1), key='privilege')],
            [sg.OK(size=(10, 1)), sg.Cancel(size=(10, 1))]
        ]

        window = sg.Window(title, auto_size_text=False, default_element_size=(15,1),
                           text_justification='right', ).Layout(layout)

        while True:
            event, values = window.Read()
            if event in [None, 'Cancel']:
                sys.exit()
            else:
                if values['password_1'] == values['password_2']:
                    window.Close()
                    sg.PopupOK('User Created Succesfully')
                    return values['username'], values['password_1'], values['privilege']
                else:
                    sg.Popup('Passwords mismatch!')

    @staticmethod
    def delete_user_window(host, user_list):
        """Prompts the user with a form for deleting a user from a list of users."""
        title = f'Delete an user from {host}'

        layout = [[sg.T('Choose an user to delete:')]]
        layout += [[sg.Radio(f'{user}', 'RADIO4', key=f'{user}')] for user in user_list]
        layout += [[sg.OK('DELETE', size=(10, 1)), sg.Cancel(size=(10, 1))]]

        window = sg.Window(title, layout)

        while True:
            event, values = window.Read()
            if event in [None, 'Cancel']:
                sys.exit()
            else:
                choice = sg.PopupOKCancel('Are you sure?')
                if len(user_list) == 1:
                    sg.Popup("Can't delete the only user left")
                elif choice == 'OK':
                    sg.Popup(f'User deleted!')
                    window.Close()
                    break
                elif choice in [None, 'Cancel']:
                    continue

        for key, value in values.items():
            if value == True:
                return key


    @staticmethod
    def secure_configuration_window(host, current_clock, hostname, domain, users):
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
             sg.Spin(values=[i for i in range(30)], initial_value='3', size=(2, 1), key='ssh_timeout_min'),
             sg.T('seconds'),
             sg.Spin(values=[i for i in range(60)], initial_value='0', size=(2, 1), key='ssh_timeout_sec')],
            [sg.T('Console exec timeout', size=(17, 1)),
             sg.T('minutes'),
             sg.Spin(values=[i for i in range(30)], initial_value='3', size=(2, 1), key='con_timeout_min'),
             sg.T('seconds'),
             sg.Spin(values=[i for i in range(60)], initial_value='0', size=(2, 1), key='con_timeout_sec')],
            [sg.T('Banner')],
            [sg.Multiline(size=(35, 3), key='banner', default_text='/Default Banner/')],
            [sg.Frame(layout=[
                [sg.T('ACL Name', size=(8, 1)), sg.In(size=(20, 1), key='acl_name')],
                [sg.T('Remark', size=(8, 1)), sg.In(size=(20, 2), key='acl_remark')],
                [sg.T('Permit', size=(8, 1)),
                 sg.T('IP'), sg.In(size=(15, 1), key='ip'),
                 sg.T('Wildcard'), sg.In(size=(15, 1), key='wildcard')],
            ], title='Access Control')],
            [sg.T('Delay between successive failed logins'),
             sg.Spin(values=[i for i in range(11)], initial_value='3', size=(2, 1), key='login_delay'),
             sg.T('seconds')],
            [sg.Checkbox('Log successful logins', key='log_success_login')],
            [sg.Checkbox('Log failed logins', key='log_failure_login')],
            [sg.OK()]
        ]

        #TODO: user input validation

        window = sg.Window(title, layout)

        event, values = window.Read()
        window.Close()

        return event, values

    @staticmethod
    def progress_bar_window(host):
        """Displays a progress bar that informs the user on the currently running processes."""

        title = f'Fetching device information from {host}'
        layout = [
            [sg.ProgressBar(1, orientation='h', size=(40, 10), key='progress')]
        ]
        window = sg.Window(title, layout,
                           auto_size_text=False,
                           default_element_size=(10,1)).Finalize()
        progress = window.FindElement('progress')

        return progress

    @staticmethod
    def save_configuration_window():
        """Propmts the user with the choice to save the configuration to flash."""

        title = 'Save Configuration'

        layout = [
            [sg.T('Save Configuration to flash?', size=(20, 1))],
            [sg.Radio('Yes', 'RADIO3', size=(5, 1), key='yes'),
             sg.Radio('No', 'RADIO3', size=(5, 1), key='no')],
            [sg.OK('Confirm', size=(10, 1)), sg.Cancel(size=(10, 1))]
        ]

        window = sg.Window(title, layout,
                           auto_size_text=False,
                           default_element_size=(10, 1),
                           element_justification='center')

        while True:
            event, values = window.Read()
            if event is None:
                sys.exit()
            else:
                if values['yes']:
                    window.Close()
                    sg.Popup('Configuration saved to flash')
                    return True
                elif values['no'] or event == 'Cancel':
                    choice = sg.PopupOKCancel('All changes will be lost at reboot.\nAre you sure?')
                    if choice in ['Cancel', None]:
                        continue
                    elif choice == 'OK':
                        window.Close()
                        sg.Popup('Configuration not saved to flash')
                        return False
