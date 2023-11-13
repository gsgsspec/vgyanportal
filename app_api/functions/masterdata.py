
from app_api.models import Registration


def auth_user(user_mail):
    try:
        return Registration.objects.get(email=user_mail)

    except Exception as e:
        raise