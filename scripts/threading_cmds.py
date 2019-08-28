import threading
from datetime import datetime
from my_devices import device_list as devices
from gui import *
from show_cmds import *
from set_cmds import set_clock


def main(func):
    """
    Use threads and Netmiko to connect to each of the devices.
    Execute commands definded in 'func' on each device.
    Record the ammount of time required to do this.
    """
    start_time = datetime.now()

    for device in devices:
        username, password, secret = get_credentials(device['host'])
        device['username'] = username
        device['password'] = password
        device['secret'] = secret
        my_thread = threading.Thread(target=func, args=(device,))
        my_thread.start()

    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()

    print('\nElapsed time:' + str(datetime.now() - start_time))


if __name__ == '__main__':
    # main(set_clock)
    host = '192.168.0.1'
    username, password, secret = ('admin', 'fuckasspunk', 'fuckasspunk')
    device = {
        'device_type': 'cisco_asa',
        'host': host,
        'username': username,
        'password': password,
        'secret': secret
    }
    current_clock = 'clock'
    hostname = 'hostname'
    print(form_secure_login(host, current_clock, hostname))
