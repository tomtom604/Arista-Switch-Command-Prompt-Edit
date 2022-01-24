# Arista-Switch-Command-Prompt-Edit
You can execute commands to several Arista switches all at once inside a command prompt. 

Test environment uses VirtualBox and 3 Arista VMs, all of which must be configured with the following:

1. Their own IP address (don't forget "no shutdown")
2. Username and secret set (you will be asked to use these credentials in the program)
3. (On your PC) add a Legacy loopback network adaptor, and make bridged connection on the three VMs to this adapter

Inside this repository edit the "IPaddress.txt" file with your IP addresses each on it's own line.

Execute in CMD Prompt by using the "python" command and the directory of the "NetworkApp.py" 


Arista CLI commands:

enable

configure terminal

username admin secret python

hostname Arista1

interface Management 1

ip address 10.10.10.2 255.255.255.0

no shutdown

copy run start



Arista2

enable

configure terminal

username admin secret python

hostname Arista2

interface Management 1

ip address 10.10.10.3 255.255.255.0

no shutdown

copy run start



Arista3

enable

configure terminal

username admin secret python

hostname Arista3

interface Management 1

ip address 10.10.10.4 255.255.255.0

no shutdown

copy run start
