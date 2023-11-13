from django.shortcuts import render


def loginPage(request):
    try:


        return render(request,'login.html')
    except Exception as e:
        raise