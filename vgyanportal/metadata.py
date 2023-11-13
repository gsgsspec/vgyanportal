import configparser
from .settings import BASE_DIR
import os


def getConfig():
    try:

        config = configparser.ConfigParser()
        config_file_path = os.path.normpath(os.path.join(BASE_DIR,'config.ini'))
        config.read(config_file_path)
        
        return config

    except Exception as e:
        raise