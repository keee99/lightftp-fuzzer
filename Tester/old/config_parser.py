import os,configparser,subprocess,ftplib
#from SWTesting import retrieve_account_details,retrieve_config_details,set_config

account = 'webadmin' 
configParser = configparser.RawConfigParser()
configFilePath = os.path.dirname(os.getcwd())+'/Source'+'/Release'+'/fftp.conf'
configParser.read(configFilePath)

# Retrieve config details
def retrieve_config_details():
    configDetails = dict(configParser.items('ftpconfig'))
    # print(f"config details are : \n {configDetails}")
    return configDetails

# Retrieve all username and pw from config file
def retrieve_account_details():
    usernameDict={}
    for item in configParser.sections():
        if item != "ftpconfig":
            usernameDict[item] = dict(configParser.items(item))
    # print(f"Account details : \n {usernameDict}")
    return usernameDict

# Set Config Function, section is 'ftpconfig' or username
def set_config(section, option, value):
    if configParser.has_section(section):
        configParser.set(section,option,value)
        with open(configFilePath,"w") as conf_file:
            configParser.write(conf_file)
            return True