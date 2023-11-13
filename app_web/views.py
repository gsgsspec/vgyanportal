from django.shortcuts import render


def loginPage(request):
    try:

        return render(request,'login.html')
    
    except Exception as e:
        raise


def myCourses(request):
    try:

        return render(request,'index.html',{'template_name':'myCourses.html'})
    except Exception as e:
        raise