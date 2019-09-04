[![Generic badge](https://img.shields.io/badge/python_version-3.7-blue.svg)](https://shields.io/)
# Netmiko_scripts


Python Scripts for network automation powered by Netmiko!

In the **_scripts_** folder you will find a wide variety of useful network automation scripts that I have developed to
help me automate network switches, routers and firewalls configuration, back-ups and statistics.


### Methods implemented up to date:
 - .version() - execute _show version_ command and print out the response.
 - .clock - getter and setter for clock information
 - .hostname - getter and setter for hostname information
 - .domain - getter and setter for domain information
 - .get_users() - returns a list of configured users
 - .add_user() - creates a new user via gui interface
 - .delete_user() - deletes a user via gui interface
 - .get_current_user_privilege() - returns the privilege number for the current logged on user
 - .save_configuration() - save the device configuration to flash via gui interface

### Project structure
  __device.py__ - contains the CiscoDevice class that has methods for interacting with the device.
  __gui.py__ - contains the UserInterface class that has gui templates for device configuration.
  __my_devices.py__ - a list of all the devices. #TODO: make this a json file
  __hyperthreading.py__ - an add-on for threading tasks.
  __main_program.py__ - the place where you can combine all the tools to make magic happen.


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
