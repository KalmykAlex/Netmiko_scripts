from netmiko import ConnectHandler


def show_version(device):
    """Execute show version command using Netmiko."""
    with ConnectHandler(**device) as remote_conn:
        print(f"Version information for: {device['host']}")
        print('~' * 100)
        print(remote_conn.send_command('show version'))


def show_clock(device):
    """Execute show clock command using Netmiko."""
    with ConnectHandler(**device) as remote_conn:
        print(f"Clock information for: {device['host']} --- ", end='')
        print(remote_conn.send_command('show clock').replace('*', ''), end='')
