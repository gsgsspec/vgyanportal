from django.shortcuts import render
from app_api.functions.masterdata import user_not_active,auth_user
from app_api.functions.services import getMyCourses, getUserProfile, getCourseDetails
from app_api.models import CourseRegistration, Registration
from django.contrib.auth import logout

def loginPage(request):
    try:

        return render(request,'login.html')
    
    except Exception as e:
        raise


def user_logout(request):
    try:
        
        logout(request)

        return render(request,'login.html')
    except Exception as e:
        raise


def coursesPage(request):
    if not request.user.is_active or not request.user.is_staff:
        return user_not_active(request, after_login_redirect_to=str(request.META["PATH_INFO"]))
    
    try:
        user_mail = request.user
        user_data = auth_user(user_mail)
        userId = user_data.id

        getCoursesList = getMyCourses(userId)
        user_details = getUserProfile(user_mail)

        return render(request,'index.html',{'template_name':'courses.html','getCoursesList':getCoursesList,'user_details':user_details})
    
    except Exception as e:
        raise


def profilePage(request):
    if not request.user.is_active or not request.user.is_staff:
        return user_not_active(request, after_login_redirect_to=str(request.META["PATH_INFO"]))
    try:

        user_mail = request.user
        user_data = getUserProfile(user_mail)

        return render(request,'index.html',{'template_name':'profile.html','user_data':user_data})
    except Exception as e:
        raise


def askQuestionPage(request):
    if not request.user.is_active or not request.user.is_staff:
        return user_not_active(request, after_login_redirect_to=str(request.META["PATH_INFO"]))
    try:

        user_mail = request.user
        user_data = getUserProfile(user_mail)


        return render(request,'index.html',{'template_name':'ask_question.html','user_details':user_data})
    except Exception as e:
        raise

def ratingPage(request):
    if not request.user.is_active or not request.user.is_staff:
        return user_not_active(request, after_login_redirect_to=str(request.META["PATH_INFO"]))
    
    try:

        return render(request, 'index.html',{'template_name':'rating.html'})
    except Exception as e:
        raise


def courseDetailsPage(request,cid):
    if not request.user.is_active or not request.user.is_staff:
        return user_not_active(request, after_login_redirect_to=str(request.META["PATH_INFO"]))
    
    try:
        reg_id = Registration.objects.get(email=request.user).id
        user_courses = CourseRegistration.objects.filter(registrationid=reg_id)

        if user_courses.filter(courseid=cid).exists():

            user_data = getUserProfile(request.user)
            
            course_details = getCourseDetails(request,cid)

            return render(request, 'index.html',{'template_name':'course_details.html','course_details':course_details,'user_data':user_data})
        
        else:
            return render (request,'index.html',{'template_name':'404.html'})
    
    except Exception as e:
        raise


def assessmentsPage(request):
    if not request.user.is_active or not request.user.is_staff:
        return user_not_active(request, after_login_redirect_to=str(request.META["PATH_INFO"]))
    
    try:
        user_mail = request.user
        user_data = auth_user(user_mail)
        userId = user_data.id

        user_details = getUserProfile(user_mail)

        return render(request,'index.html',{'template_name':'assessments.html','user_details':user_details})
    
    except Exception as e:
        raise