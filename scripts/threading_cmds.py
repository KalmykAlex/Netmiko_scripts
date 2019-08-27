import threading
from datetime import datetime
from my_devices import device_list as devices
from gui import get_credentials
from show_cmds import show_version, show_clock


def main(func):
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
        my_thread = threading.Thread(target=func, args=(device,))
        my_thread.start()

    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            print(some_thread)
            some_thread.join()

    print('\nElapsed time:' + str(datetime.now() - start_time))

main(show_clock)
