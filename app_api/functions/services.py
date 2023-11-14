from rest_framework.authtoken.models import Token
from .database import addUserDB
from app_api.models import Registration, User_data


def authentication_service(dataObjs):
    try:
        user = Registration.objects.get(email=dataObjs['email'],password=dataObjs['password'],status='A')
    except:
        return (None,)
    
    try:
        if user:
            check1 = User_data.objects.filter(usr_email=user.email, usr_password=user.password)
            if not check1:
                print('1')
                User_data(username=user.email, usr_email=user.email, usr_password=user.password, is_staff=True).save()
            token_obj = Token.objects.filter(user__usr_email=user.email).order_by('-created').first()
            user_data = User_data.objects.get(usr_email=user.email, usr_password=user.password)
            user_data.is_staff = True 
            user_data.save()
            if token_obj:
                return token_obj.key
            else:
                check = User_data.objects.filter(usr_email=user.email).first()
                token_obj, token_flag = Token.objects.get_or_create(user=check)
                return token_obj.key
    except Exception as e:
        print(str(e))
        raise


def addUserService(dataObjs):
    try:

        addUserDB(dataObjs)

    except Exception as e:
        raise

