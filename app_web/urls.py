from django.urls import path
from . import views


urlpatterns = [
    path('',views.loginPage),
    path('my-courses',views.myCourses)
]
