import json
from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from allauth.account.utils import perform_login
from allauth.account import app_settings as allauth_settings
from app_api.functions.masterdata import auth_user
from .functions.services import addUserService, authentication_service
from .models import User_data
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@authentication_classes([])
@permission_classes([]) 
def addUser(request):
    response ={
        'data':None,
        'error':None,
        'statusCode':1
    }
    try:

        if request.method == 'POST':
            dataObjs = json.loads(request.POST.get('data'))
            addUserService(dataObjs)
            response['data'] = "Details Saved Sucessfully"
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in Registration'
        response['error'] = str(e)
        raise

    return JsonResponse(response)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def loginView(request):
    response = {
        'data':None,
        'error':None,
        'statusCode':1
    }
    try:

        if request.method == "POST":

            dataObjs = json.loads(request.POST.get('data'))
            print('dataObjs',dataObjs)
            auth_token = authentication_service(dataObjs)
            print('auth token',auth_token)
            if auth_token[0] != None:
                usr = User_data.objects.filter(usr_email=dataObjs['email']).first()
                perform_login(request._request, usr, allauth_settings.EMAIL_VERIFICATION, signup=False,
                              redirect_url=None, signal_kwargs=None)
                user = auth_user(usr)
                print('user',user)
                response['token'] = 'token_generated'
                response['data'] = 'Successfully logged-in'
                response['login_type'] = auth_token[1]
            else:
                response['token'] = 'AnonymousUser'
                response['data'] = 'login failed'
            
            response['statusCode'] = 0


    except Exception as e:
        response['data'] = 'Error in Sign-in'
        response['error'] = str(e)
        raise
    return JsonResponse(response)