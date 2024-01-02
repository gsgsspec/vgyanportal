import configparser
from .settings import BASE_DIR
import os
from django.http import HttpResponseForbidden
from urllib.parse import urlsplit


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
        if time:
        
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



def check_referrer(request):

    try:

        if 'HTTP_REFERER' not in request.META:
            return False
        
        referrer = request.META['HTTP_REFERER']
        referrer_host = urlsplit(referrer).hostname

        allowed_referrers = ['134.122.25.72']

        if referrer_host not in allowed_referrers:
            return False

        return True
    
    except Exception as e:
        print("Error checking referrer: ", str(e))
        return False