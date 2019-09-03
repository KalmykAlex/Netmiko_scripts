from device import CiscoDevice
from gui import UserInterface as ui


if __name__ == '__main__':
    switch = CiscoDevice()
    pb = ui.progress_bar_window(switch.host)
    pb.UpdateBar(0, 4)
    with switch:
        hostname = switch.hostname
        pb.UpdateBar(1, 4)
        users = switch.get_users()
        pb.UpdateBar(2, 4)
        domain = switch.domain
        pb.UpdateBar(3, 4)
        current_clock = switch.clock
        pb.UpdateBar(4, 4)
        print(ui.secure_configuration_window(switch.host, current_clock, hostname, domain, users))
