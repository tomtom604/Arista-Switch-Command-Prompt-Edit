import paramiko
import os.path
import time
import sys
import re

#Variable for program directory
network_app_dir = os.path.abspath(os.getcwd())

#Prompting user for input - USERNAME
username_input = input("\n# Enter Username: ")

#Prompting user for password
password_input = input("\n# Enter Password: ")

#Combine user/pass into one string
user_pass_combo = "{},{}".format(username_input, password_input)

#Overwrite user/pass file
def user_pass_edt():
        
        global network_app_dir
        global user_pass_combo
        
        with open(r"{}\user.txt".format(network_app_dir), 'w') as user_pass:
            user_pass.write(user_pass_combo)
            
        user_pass = (r"{}\user.txt".format(network_app_dir))

        return user_pass


user_file = user_pass_edt()

#Verifying the validity of the USERNAME/PASSWORD file
if os.path.isfile(user_file) == True:
    print("\n* Username/password file is valid \n")

else:
    print("\n* File {} does not exist  Please check and try again.\n".format(user_file))
    sys.exit()
        
#Checking commands file
#Prompting user for input - COMMANDS FILE

print("\n* Enter in command one at a time. When finished leave blank and press enter \n") 

cmd_line = []

while True:

    cmd_input = input("\n#")
    cmd_line.append(cmd_input + ";")
    if cmd_input == "":
        break
    else:
        continue

with open(r"{}\cmd.txt".format(network_app_dir), 'w') as cmd_file:
    for cmd in cmd_line:
        cmd = cmd.replace(";", "")
        cmd_file.write(cmd)

cmd_file = (r"{}\cmd.txt".format(network_app_dir))

#Verifying the validity of the COMMANDS FILE
if os.path.isfile(cmd_file) == True:
    print("\n* Command file is valid \n")

else:
    print("\n* File {} does not exist. Please check and try again.\n".format(cmd_file))
    sys.exit()
    
#Open SSHv2 connection to the device
def ssh_connection(ip):
    
    global user_file
    global cmd_file
    
    #Creating SSH CONNECTION
    try:
        #Define SSH parameters
        selected_user_file = open(user_file, 'r')
        
        #Starting from the beginning of the file
        selected_user_file.seek(0)
        
        #Reading the username from the file
        username = selected_user_file.readlines()[0].split(',')[0].rstrip("\n")
        
        #Starting from the beginning of the file
        selected_user_file.seek(0)
        
        #Reading the password from the file
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        
        #Logging into device
        session = paramiko.SSHClient()
        
        #For testing purposes, this allows auto-accepting unknown host keys
        #Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        #Connect to the device using username and password          
        session.connect(ip.rstrip("\n"), username = username, password = password)
        
        #Start an interactive shell session on the router
        connection = session.invoke_shell()	
        
        #Setting terminal length for entire output - disable pagination
        connection.send("enable\n")
        connection.send("terminal length 0\n")
        time.sleep(1)
        
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)
        
        #Open user selected file for reading
        selected_cmd_file = open(cmd_file, 'r')
            
        #Starting from the beginning of the file
        selected_cmd_file.seek(0)
        
        #Writing each line in the file to the device
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + '\n')
            time.sleep(2)
        
        #Closing the user file
        selected_user_file.close()
        
        #Closing the command file
        selected_cmd_file.close()
        
        #Checking command output for IOS syntax errors
        router_output = connection.recv(65535)
        new_output = str(router_output).replace(r"\r", "\n")
        newest_output = new_output.replace(r"\n", "\n")
        
        if re.search(b"% Invalid input", router_output):
            print("* There was at least one IOS syntax error on device {} ".format(ip))
            
        else:
            print("\nDONE for device {} \n".format(ip))
            print(new_output + "\n *** \n")
        
        #Closing the connection
        session.close()
     
    except paramiko.AuthenticationException:
        print("* Invalid username or password :( \n* Please check the username/password file or the device configuration.")
        print("* Closing program... Bye!")