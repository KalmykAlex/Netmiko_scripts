import threading


def hyper_list(func):
    """
    Use threads and Netmiko to connect to each of the devices.
    Execute commands definded in 'func' on each device.
    """

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


#TODO: Threading for commands executed on same device