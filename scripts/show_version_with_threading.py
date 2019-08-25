import threading
from netmiko import ConnectHandler
from datetime import datetime
from my_devices import device_list as devices
from pysimplegui_credentials import get_credentials


def show_version(device):
    """Execute show version command using Netmiko."""
    remote_conn = ConnectHandler(**device)
    print()
    print('#' * 80)
    print(remote_conn.send_command_expect('show version'))
    print('#' * 80)
    print()
    remote_conn.disconnect()

def main():
    """
    Use threads and Netmiko to connect to each of the devices. Execute
    'show version' on each device. Record the ammount of time required to do this.
    """
    start_time = datetime.now()

    for device in devices:
        username, password, secret = get_credentials(device.pop('device_name'))
        device['username'] = username
        device['password'] = password
        device['secret'] = secret
        my_thread = threading.Thread(target=show_version, args=(device,))
        my_thread.start()

    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            print(some_thread)
            some_thread.join()

    print('\nElapsed time:' + str(datetime.now() - start_time))

main()
