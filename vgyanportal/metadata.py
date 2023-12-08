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



def change_timeformat(time,type):
    try:
        
        if time <= 3600:

            minutes, seconds = divmod(time, 60)
            if type == 'L':
                return f"{int(minutes):02d}:{int(seconds):02d}"
            else:
                return f"{int(minutes):02d} min"

        else:
            hours, remainder = divmod(time, 3600)
            minutes, seconds = divmod(remainder, 60)
            if type == 'L':
                return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            else:
                return f"{int(hours):01d}hr {int(minutes):02d}min"
           

    except Exception as e:
        raise