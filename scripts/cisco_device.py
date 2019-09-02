from netmiko import ConnectHandler
from datetime import datetime
from gui import get_device, get_credentials, get_device_type
from re import search
import pytz


class Device:

    def __init__(self):
        device_type = get_device_type()
        self.host = get_device()
        username, password, secret = get_credentials(self.host)
        self.device = {
            'device_type': device_type,
            'host': self.host,
            'username': username,
            'password': password,
            'secret': secret
        }

    def __enter__(self):
        self.remote_conn = ConnectHandler(**self.device)
        return self

    def version(self):
        """Execute show version command."""
        print(f"Version information for: {self.device['host']}")
        print('~' * 100)
        print(self.remote_conn.send_command('show version'))

    @property
    def clock(self):
        """Returns the time and date on the device."""
        print(f"Fetching time information from {self.device['host']}")
        clock_str = self.remote_conn.send_command('show clock').replace('*', '').strip()
        clock = datetime.strptime(clock_str, '%H:%M:%S.%f %Z %a %b %d %Y')
        clock_utc = pytz.utc.localize(clock)
        return clock_utc.strftime('%H:%M:%S %Z %a %b %d %Y')

    @clock.setter
    def clock(self, datetime_obj):
        """
        Sets the clock of the device using Netmiko.
        :param datetime_obj: an instance of the datetime.datetime class
        """
        if isinstance(datetime_obj, datetime):
            equipment_date_raw = self.remote_conn.send_command('show clock') \
                .replace('*', '').strip()
            equipment_date = datetime.strptime(
                equipment_date_raw,
                '%H:%M:%S.%f %Z %a %b %d %Y'
            )

            timedelta = abs((equipment_date - datetime_obj).total_seconds())

            if timedelta > 30:
                date = datetime_obj.strftime('%H:%M:%S %d %b %Y')
                print(f"{self.device['host']} - \
                        Clock Offset: {timedelta} seconds. \
                        Setting clock: {date}"
                      )
                self.remote_conn.enable()
                self.remote_conn.send_command(f'clock set {date}')
            else:
                print(f"{self.device['host']} - {equipment_date_raw} - Clock OK")
        else:
            raise ValueError('Must assign a datetime object.')

    @property
    def hostname(self):
        """Returns the hostname of the device."""
        print(f"Fetching hostname information from {self.device['host']}")
        name = self.remote_conn.find_prompt().replace('#', '')
        return name

    @hostname.setter
    def hostname(self, name):
        """
        Sets the hostname of the device.
        :param name: string that must contain at least one alphabet or '-' or '_' character
        """
        if search('[a-zA-z_-]', name):
            print(f'Setting hostname {name} to {self.host}')
            self.remote_conn.send_command(f'hostname {name}')
            self.remote_conn.send_command('end')
            print(self.remote_conn.find_prompt())
        else:
            raise ValueError("Hostname should contain at least one alphabet or '-' or '_' character")


    def users(self):
        """Returns a list of configured users."""
        print(f"Fetching users information from {self.device['host']}")
        users_str = self.remote_conn.send_command('show running-config | include username').split('\n')
        user_list = []
        for line in users_str:
            user_list.append(line.split()[1])
        return user_list

    def domain(self):
        """Returns the domain name configured on the device."""
        print(f"Fetching domain information from {self.device['host']}")
        return self.remote_conn.send_command('show running-config | include domain').split()[-1]

    def __exit__(self, *args):
        while True:
            choice = input('Save changes to flash? (Y/N): ')
            if choice in ['Y', 'y', 'yes']:
                self.remote_conn.enable()
                self.remote_conn.send_command('write memory')
                print('Configuration saved to flash.')
                break
            elif choice in ['N', 'n', 'no']:
                print('Configuration not saved to flash. All changes will be lost at reboot.')
                break
            else:
                print('Invalid option selected.\nPlease try again.')
        self.remote_conn.disconnect()
