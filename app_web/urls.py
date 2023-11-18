from django.urls import path
from . import views


urlpatterns = [
    path('',views.loginPage),
    path('courses',views.coursesPage),
    path('profile',views.profilePage),
    path('ask-question',views.askQuestionPage)
]
