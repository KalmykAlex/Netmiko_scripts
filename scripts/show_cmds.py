from netmiko import ConnectHandler
from datetime import datetime
from gui import get_device, get_credentials
import pytz

class Device(object):

    def __init__(self):
        self.host = get_device()
        username, password, secret = get_credentials(self.host)
        self.device = {
            'device_type': 'cisco_asa',
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


    def clock(self):
        """Returns the time and date on the device."""
        print(f"Fetching time information from {self.device['host']}")
        clock_str = self.remote_conn.send_command('show clock').replace('*', '').strip()
        clock = datetime.strptime(clock_str, '%H:%M:%S.%f %Z %a %b %d %Y')
        clock_utc = pytz.utc.localize(clock)
        return clock_utc.strftime('%H:%M:%S %Z %a %b %d %Y')


    def hostname(self):
        """Returns the hostname of the device."""
        print(f"Fetching hostname information from {self.device['host']}")
        hostname = self.remote_conn.find_prompt().replace('#', '')
        return hostname


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
        self.remote_conn.disconnect()
