import os
import logging
import configparser


class Config():
    def __init__(self) -> None:
        self.uname = None
        self.pwd = None
        self.addr = None
        self.port = None
        


# This class is responsible for parsing the ftpconfig file
class ConfigParser:

    DEFAULT_ACCT = "webadmin"
    
    @classmethod
    def get_config(cls, config_dir: str, account: str) -> Config:

        # Init new config parser
        configParser = configparser.RawConfigParser()
        print(config_dir)
        configParser.read(config_dir)
        configDetails = dict(configParser.items('ftpconfig'))

        usernameDict={}
        for item in configParser.sections():
            if item != "ftpconfig":
                usernameDict[item] = dict(configParser.items(item))


        config = Config()

        config.uname = account                      # 'webadmin'
        config.pwd = usernameDict[account]['pswd']  # 'password'
        config.addr = configDetails['interface']    # '127.0.0.1'
        config.port = configDetails['port']         # '8080'
        
        logger = logging.getLogger()
        logger.info(f"account: \n {account}")
        logger.info(f"pswd: \n {config.pwd}")
        logger.info(f"host: \n {config.addr}")
        logger.info(f"port: \n {config.port}")

        return config

        
        


def set_config(config_dir: str, section: str, option: str, value: str) -> bool:
    configParser = configparser.RawConfigParser()
    configFilePath = os.path.dirname(os.getcwd()) + config_dir
    configParser.read(configFilePath)
    
    if configParser.has_section(section):
        configParser.set(section, option, value)
        try:
            with open(configFilePath,"w") as conf_file:
                configParser.write(conf_file)
                return True
        except OSError:
            return False


