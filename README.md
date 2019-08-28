# Netmiko_scripts

Python Scripts for network automation powered by Netmiko!

In the **_scripts_** folder you will find a wide variety of useful network automation scripts that I have developed to
help me automate network switches, routers and firewalls configuration, back-ups and statistics.


### Scripts implemented up to date:
 - get version information from devices
 - get clock information from devices
 - automatic clock update on device with clock offset greater than 30 secs
 

### Usage description
 1. You will need to define all of your devices in **my_devices.py**.
 2. In **threading_cmds.py** you will need to pass whichever function you want to the main() function.
  function examples: show_clock, show_version, set_clock etc.
 3. After you run the script a pop-up will appear asking you for login credentials for each device.


### Devices tested | results: 
I primarily focus on Cisco equipment but I am experimenting with other brands also.
 - [X] Cisco C2960-24TC-S Switch | works fine
 - [ ] Cisco C2950T-48-SI Switch | could work but my IOS version doesn't support SSH
 - [ ] Cisco SF300-24 Switch | doesn't work, unsupported netmiko firmware
 - [ ] Allied Telesis AT-9000/24 Switch (experimental) | doesn't work, unsupported netmiko firmware
 - [X] Cisco ASA 5506 | works fine
 - [ ] Cisco ASA 5508 | not yet tested
 - [ ] Cisco ASA 5545 | not yet tested
 
 
 ### Setting up SSH connection first
 
 For the scripts to work, you must first make some basic configuration on the device in order for Netmiko to be able to connect to the
 device via SSH.
 
 Example for basic config for a cisco switch:
 ```
  ip default-gateway <gateway IP address>

  interface vlan <vlan number>
    ip address <IP address> <netmask>
    no shutdown
    exit

  hostname <name>
  ip domain-name <domain name>

  crypto key generate rsa
    How many bits in the modulus [512]: 2048

  line vty 0 4
    transport input ssh
    login local
    exit
  line console 0
    logging synchronous
    login local
    exit

  username <name> password <password>
  enable secret <enable password>
  service passowrd-encryption

  # Checking that SSH works
  sh ip ssh
    SSH Enabled - version 1.99
    Authentication timeout: 120 secs; Authentication retries: 3
```
