from django.shortcuts import render
from app_api.functions.masterdata import user_not_active


def loginPage(request):
    try:

        return render(request,'login.html')
    
    except Exception as e:
        raise


def coursesPage(request):
    if not request.user.is_active or not request.user.is_staff:
        
        return user_not_active(request, after_login_redirect_to=str(request.META["PATH_INFO"]))
    
    try:
        
        return render(request,'index.html',{'template_name':'courses.html'})
    except Exception as e:
        raise