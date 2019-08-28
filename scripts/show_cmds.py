from netmiko import ConnectHandler
from datetime import datetime
import pytz


def show_version(device):
    """Execute show version command."""
    with ConnectHandler(**device) as remote_conn:
        print(f"Version information for: {device['host']}")
        print('~' * 100)
        print(remote_conn.send_command('show version'))


def show_clock(device):
    """Execute show clock command."""
    with ConnectHandler(**device) as remote_conn:
        print(f"Clock information for: {device['host']} --- ", end='')
        print(remote_conn.send_command('show clock').replace('*', ''), end='')


def get_clock(device):
    """Returns the time and date on the device."""
    with ConnectHandler(**device) as remote_conn:
        clock_str = remote_conn.send_command('show clock').replace('*', '').strip()
        clock = datetime.strptime(clock_str, '%H:%M:%S.%f %Z %a %b %d %Y')
        clock_utc = pytz.utc.localize(clock)
        return clock_utc.strftime('%H:%M:%S %Z %a %b %d %Y')


def get_hostname(device):
    """Returns the hostname of the device."""
    with ConnectHandler(**device) as remote_conn:
        hostname = remote_conn.find_prompt().replace('#', '')
        return hostname