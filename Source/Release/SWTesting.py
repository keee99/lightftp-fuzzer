# Assume run on Ubuntu 18.04 and necessary libraries are installed
# Read fftp.conf
import configparser
import os
import getpass
import subprocess

account = 'webadmin' 
ubuntuPassword = '123456'

configParser = configparser.RawConfigParser()
configFilePath = r'./fftp.conf'
configParser.read(configFilePath)

# Prompting sudo password in the beginning
sudo_password = getpass.getpass(prompt='sudo password: ')
p = subprocess.Popen(['sudo', '-S', 'ls'], stderr=subprocess.PIPE, stdout=subprocess.PIPE,  stdin=subprocess.PIPE)

try:
    out, err = p.communicate(input=(sudo_password+'\n').encode(),timeout=5)

except subprocess.TimeoutExpired:
    p.kill()

# Retrieve config details
def retrieve_config_details():
    configDetails = dict(configParser.items('ftpconfig'))
    print(f"config details are : \n {configDetails}")
    return configDetails

# Retrieve all username and pw from config file
def retrieve_account_details():
    usernameDict={}
    for item in configParser.sections():
        if item != "ftpconfig":
            usernameDict[item] = dict(configParser.items(item))
    print(f"Account details : \n {usernameDict}")
    return usernameDict

# Set Config Function, section is 'ftpconfig' or username
def set_config(section, option, value):
    if configParser.has_section(section):
        configParser.set(section,option,value)
        with open(configFilePath,"w") as conf_file:
            configParser.write(conf_file)
            return True

# Check port in cfg file is not 21 and change to 80 if it is
configDetails = retrieve_config_details()
if configDetails['port']==21:
    set_config('ftpconfig',"port",8080)

# Retrieve local target folder
accountDetails = retrieve_account_details()
target_folder = accountDetails[account]['root']

ipAddress,port = configDetails['interface'], configDetails['port']

if not os.path.exists(target_folder):
    os.mkdir(target_folder)

# Start Server
subprocess.Popen(os.system("sudo ./fftp"))
