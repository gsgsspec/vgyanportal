
import os
import secrets
import string
from vgyanportal import settings
from app_api.models import Registration, User_data
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


def saveProfileDetailsDB(dataObjs, fileObjs):
    try:

        user_profile = Registration.objects.get(email=dataObjs['email'])
        user_profile.firstname = dataObjs['firstname']
        user_profile.lastname = dataObjs['lastname']
        user_profile.password = dataObjs['password']
        user_profile.country = dataObjs['country']

        user_img = fileObjs.get('file')

        if user_img:

            img_file = os.path.splitext(user_img.name)
            img_extension = img_file[1]

            user_img_name = f"{user_profile.id}_{user_profile.firstname}{img_extension}"
            img_path = os.path.join(settings.MEDIA_ROOT,'user_profile',user_img_name)

            with open(img_path, 'wb+') as user_image:
                for chunk in user_img.chunks():
                    user_image.write(chunk)

            user_profile.profilepicurl = f"user_profile/{user_img_name}"
        
        user_profile.save()

        user_auth = User_data.objects.get(usr_email=dataObjs['email'])
        user_auth.usr_password = dataObjs['password']
        user_auth.save()

    except Exception as e:
        raise