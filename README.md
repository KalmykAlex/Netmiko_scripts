# Netmiko_scripts

Python Scripts for network automation powered by Netmiko!

In the **_scripts_** folder you will find a wide variety of useful network automation scripts that I have developed to
help me automate network switches, routers and firewalls configuration, back-ups and statistics.

I primarily focus on Cisco equipment but I am experimenting with other brands also.

Devices tested | results: 
 - [X] Cisco C2960-24TC-S Switch | works fine
 - [ ] Cisco C2950T-48-SI Switch | could work but my IOS version doesn't support SSH
 - [ ] Cisco SF300-24 Switch | doesn't work, unsupported netmiko firmware
 - [ ] Allied Telesis AT-9000/24 Switch (experimental) | doesn't work, unsupported netmiko firmware
 - [X] Cisco ASA 5506 | works fine
 - [ ] Cisco ASA 5508 | not yet tested
 - [ ] Cisco ASA 5545 | not yet tested
 
 For this to work, you must first make some basic configuration on the device in order for Netmiko to be able to connect to the
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
