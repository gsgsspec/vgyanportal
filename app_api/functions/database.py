

import secrets
import string
from app_api.models import Registration
from datetime import datetime
from  .mailing import sendRegistrainMail


def addUserDB(dataObjs):
    try:

        user_email = dataObjs['email']

        user_check = Registration.objects.filter(email=user_email)

        if user_check :
            print('abc')
        else:
            
            random_password = generate_random_password()
            
            registration = Registration(
                firstname = dataObjs['first_name'],
                lastname = dataObjs['last_name'],
                email = dataObjs['email'],
                password = random_password,
                dateregistered = datetime.now(),
                status = 'A'
            )

            registration.save()
            print('registration',registration.email)
            sendRegistrainMail()

    except Exception as e:
        print(str(e))
        raise


def generate_random_password(length=15):
    try:
        characters = string.ascii_letters + string.digits + string.punctuation

        password = ''.join(secrets.choice(characters) for _ in range(length))

        return password
    
    except Exception as e:
        raise


