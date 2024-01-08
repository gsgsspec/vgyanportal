import json
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from allauth.account.utils import perform_login
from allauth.account import app_settings as allauth_settings
from app_api.functions.masterdata import auth_user
from .functions.services import addUserService, authentication_service, saveProfileDetails, getModuleLessonService, saveCourseRating, saveAskQuestion, getAskQuestion, \
        getlessonVideoService, saveAssessmentService, updateAssessmentService, saveVideoActivityService,courseModuleNameService,assessmentListService,allNotificationsList,\
        removeNotificationService,markAsReadNotificationService,checkLatestNotificationsService
from .models import User_data
from django.views.decorators.csrf import csrf_exempt
from vgyanportal.metadata import check_referrer
from app_api.functions.database import updateLessonStatusDB


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
            auth_token = authentication_service(dataObjs)
            if auth_token[0] != None:
                usr = User_data.objects.filter(usr_email=dataObjs['email']).first()
                perform_login(request._request, usr, allauth_settings.EMAIL_VERIFICATION, signup=False,
                              redirect_url=None, signal_kwargs=None)
                user = auth_user(usr)
                
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



@api_view(['POST'])
def saveProfile(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST" and check_referrer(request):
            fileObjs = request.FILES
            dataObjs = json.loads(request.POST.get('data'))
            saveProfileDetails(dataObjs, fileObjs)
            response['data'] = "Profile Details Saved Sucessfully"
            response['statusCode'] = 0

        else:
            return HttpResponseForbidden('Request Blocked')
     
    except Exception as e:
        response['data'] = 'Error in save profile'
        response['error'] = str(e)
        raise
    return JsonResponse(response)



@api_view(['POST'])
def saveRating(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user
            course_rating = saveCourseRating(dataObjs,user)
            response['data'] = course_rating
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving Course rating'
        response['error'] = str(e)
        raise
    return JsonResponse(response)
    

@api_view(['POST'])
def getModuleLesson(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            getModulesLessons = getModuleLessonService(dataObjs)
            response['data'] = getModulesLessons
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in getModuleLesson'
        response['error'] = str(e)
        raise
    return JsonResponse(response)



@api_view(['POST'])
def saveQuestion(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))

            dataObjs['userId'] = request.user
            saveAskQuestion(dataObjs)

            response['data'] = 'Question Saved'
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saveQuestion'
        response['error'] = str(e)
        raise
    return JsonResponse(response)



@api_view(['POST'])
def getQuestion(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))

            userId = request.user
            
            getquestionsList = getAskQuestion(dataObjs,userId)

            response['data'] = getquestionsList
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saveQuestion'
        response['error'] = str(e)
        raise
    return JsonResponse(response)



@api_view(['POST'])
def getlessonVideoDetails(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user
            lesson_video = getlessonVideoService(dataObjs,user)
            response['data'] = lesson_video
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving Course rating'
        response['error'] = str(e)
        raise
    return JsonResponse(response)


@api_view(['POST'])
def saveAssessmentDetails(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user
            saveAssessmentService(dataObjs,user)
            response['data'] = 'Assessment details saved successfully'
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving Course rating'
        response['error'] = str(e)
        raise
    return JsonResponse(response)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def updateAssessmentDetails(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            request_data = dict(request.POST)
            dataObjs = {key: request_data[key][0] if request_data[key] else '' for key in request_data}
            updateAssessmentService(dataObjs)
            response['data'] = 'Assessment details updated successfully'
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving assessment details'
        response['error'] = str(e)
        raise
    return JsonResponse(response)


@api_view(['POST'])
def saveVideoActivity(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user
            saveVideoActivityService(dataObjs,user)
            response['data'] = 'Video activity saved successfully'
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving video activity'
        response['error'] = str(e)
        raise
    return JsonResponse(response)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def courseModuleName(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        dataObjs = request.data
        dataObjs = json.dumps(dataObjs)

        data = json.loads(dataObjs)

        course = data['coursid']
        module = data['modid']

        coursetitels = courseModuleNameService(course, module)

        response['courseTitles'] = coursetitels
        response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in courseModuleName'
        response['error'] = str(e)
        raise
    return JsonResponse(response)

@api_view(['POST'])
def assessmentslist(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user
            assessmentListService(dataObjs,user)

            response['data'] = 'Video activity saved successfully'
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving video activity'
        response['error'] = str(e)
        raise
    return JsonResponse(response)

@api_view(['POST'])
def allNotifications(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1,
        'data2'     : 'N'
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user

            notificationsList = allNotificationsList(dataObjs,user)

            response['data'] = notificationsList[0]
            response['data2'] = notificationsList[1]
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving video activity'
        response['error'] = str(e)
        raise
    return JsonResponse(response)


@api_view(['POST'])
def removeNotification(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user
            notificationsList = removeNotificationService(dataObjs,user)

            response['data'] = notificationsList
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving video activity'
        response['error'] = str(e)
        raise
    return JsonResponse(response)



@api_view(['POST'])
def markAsReadNotification(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }

    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user

            markAsReadNotificationService(dataObjs,user)
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving video activity'
        response['error'] = str(e)
        raise
    return JsonResponse(response)



@api_view(['POST'])
def updateLessonStatus(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user

            updateLessonStatusDB(dataObjs,user)

            response['data'] = 'Lesson status updated successfully'
            response['statusCode'] = 0
    except Exception as e:
        response['data'] = 'Error in updating lesson status'
        response['error'] = str(e)
        raise
    return JsonResponse(response)



@api_view(['POST'])
def checkLatestNotifications(request):
    response = {
        'data': None,
        'error': None,
        'statusCode': 1
    }
    try:
        if request.method == "POST":
            dataObjs = json.loads(request.POST.get('data'))
            user = request.user

            count =  checkLatestNotificationsService(dataObjs,user)

            response['data'] = count
            response['statusCode'] = 0

    except Exception as e:
        response['data'] = 'Error in saving video activity'
        response['error'] = str(e)
        raise
    return JsonResponse(response)
