from cisco_device import Device
from gui import form_secure_login, progress_bar
from datetime import datetime


if __name__ == '__main__':
    switch = Device()
    with switch:
        switch.hostname = 'switch'

    # pb = progress_bar(switch.host)
    # pb.UpdateBar(0, 4)
    #
    # with switch:
    #     current_clock = switch.clock
    #     pb.UpdateBar(1, 4)
    #     hostname = switch.hostname()
    #     pb.UpdateBar(2, 4)
    #     users = switch.users()
    #     pb.UpdateBar(3, 4)
    #     domain = switch.domain()
    #     pb.UpdateBar(4, 4)


    # print(form_secure_login(switch.host, current_clock, hostname, domain, users))