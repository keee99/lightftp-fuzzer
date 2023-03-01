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

# Check port in cfg file is not 21 and change to 80 if it is
# configDetails = retrieve_config_details()
# if configDetails['port']==21:
#     set_config('ftpconfig',"port",8080)

# Retrieve local target folder
# accountDetails = retrieve_account_details()
# target_folder = accountDetails[account]['root']

# ipAddress,port = configDetails['interface'], configDetails['port']
# pswd = accountDetails[account]['pswd']

#  METHOD 1 : using ftp linux command ; PROBLEM : how to answer ftp prompt?
# os.system(f'ftp ftp://{account}:{pswd}@{ipAddress}:{port}')


# Read terminal prompt after ftp starts DOESNT WORK
# result = subprocess.run(['ftp', f'ftp://{account}:{pswd}@{ipAddress}:{port}'], stdout=subprocess.PIPE).stdout.decode('utf-8')
# print(result)

# METHOD 2 : USING FTP LIBRARY
# with ftplib.FTP() as ftp:
#     ftp.connect(host=ipAddress,port=int(port))
#     ftp.login(account,accountDetails[account]['pswd'])
#     ftp.mkd('newdir')
#     ftp.dir()

# METHOD 3 : RUNNING TXT SCRIPT not sure how to apply
# os.system('ftp -n -s:ftp.txt')

