from netmiko import ConnectHandler
from datetime import datetime


def set_clock(device):
    """Sets the clock of devices using Netmiko"""
    with ConnectHandler(**device) as remote_conn:
        current_date = datetime.utcnow()
        equipment_date_raw = remote_conn.send_command('show clock')\
            .replace('*', '').strip()
        equipment_date = datetime.strptime(
            equipment_date_raw,
            '%H:%M:%S.%f %Z %a %b %d %Y'
        )

        timedelta = abs((equipment_date - current_date).total_seconds())

        if timedelta > 30:
            date = datetime.utcnow().strftime('%H:%M:%S %d %b %Y')
            print(f"{device['host']} - \
                Clock Offset: {timedelta} seconds. \
                Setting clock: {date}"
                )
            remote_conn.enable()
            remote_conn.send_command(f'clock set {date}')
        else:
            print(f"{device['host']} - {equipment_date_raw} - Clock OK")
