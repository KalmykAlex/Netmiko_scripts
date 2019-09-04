[![Generic badge](https://img.shields.io/badge/python_version-3.7-blue.svg)](https://shields.io/)
# Netmiko_scripts

Python Scripts for network automation powered by Netmiko!

In the **_scripts_** folder you will find a wide variety of useful network automation scripts that I have developed to
help me automate network switches, routers and firewalls configuration, back-ups and statistics.

___
### Project structure
 - __device.py__ - contains the __CiscoDevice__ class that has methods for interacting with the device.
 - __gui.py__ - contains the __UserInterface__ class that has gui templates for device configuration.
 - __my_devices.py__ - a list of all the devices. #TODO: make this a json file
 - __hyperthreading.py__ - an add-on for threading tasks.
 - __main_program.py__ - the place where you can combine all the tools to make magic happen.
 
___
### Methods implemented up to date:
 - __version()__ - execute _show version_ command and print out the response.
 - __clock__ - getter and setter for clock information
 - __hostname__ - getter and setter for hostname information
 - __domain__ - getter and setter for domain information
 - __get_users()__ - returns a list of configured users
 - __add_user()__ - creates a new user via gui interface
 - __delete_user()__ - deletes a user via gui interface
 - __get_current_user_privilege()__ - returns the privilege number for the current logged on user
 - __save_configuration()__ - save the device configuration to flash via gui interface

___
### List of GUI's created up to date:
 - __get_device_window()__ - prompts for IP so it knows with whom to establish an SSH connection
 - __get_device_type_window()__ - prompts for the device type (currently only cisco IOS and cisco ASA devices are supported)
 - __get_credentials_window(*host*)__ - prompts for the username, password and secret for the *host*
 - __add_user_window(*host*, *logged_on_priv*)__ - prompts for a new username (privilege level not higher that currently logged on user privilege)
 - __delete_user_window(*host*, *user_list*)__ - propts for a username to be deleted from the *user_list*
 - __secure_configuration_window(*host*, *current_clock*, *hostname*, *domain*, *user_list*)__ - a more complex window used for basic secure configuration of the device
 - __progress_bar_window(*host*)__ - a simple progress bar window
 - __save_configuration_window()__ - window for chosing to save device configuration to flash

___
### Usage description
 You are free to use the methods created in the device.CiscoDevice class however you want to acomplish your task.
 Feel free to use the predefined GUI interfaces from gui.UserInterface class.

#### Key notes:
- when you instantiate an object of the CiscoDevice class it will call the __init__ method that will prompt for device, IP and user credentials.
- the CiscoDevice class has a __start__ and a __exit__ method that you can take advantage in a context manager using the __with__ command. In this way you will not need to take care of manually tearing down the connection with the device.

___
### Devices tested | results: 
I primarily focus on Cisco equipment but I am experimenting with other brands also.
 - [X] Cisco C2960-24TC-S Switch | works fine
 - [ ] Cisco C2950T-48-SI Switch | could work but my IOS version doesn't support SSH
 - [ ] Cisco SF300-24 Switch | doesn't work, unsupported netmiko firmware
 - [ ] Allied Telesis AT-9000/24 Switch (experimental) | doesn't work, unsupported netmiko firmware
 - [X] Cisco ASA 5506 | works fine
 - [ ] Cisco ASA 5508 | not yet tested
 - [ ] Cisco ASA 5545 | not yet tested
 
 ___
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
___
