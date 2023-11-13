from django.urls import path
from app_api import views


urlpatterns = [
    path('add-user',views.addUser),
    path('login',views.loginView)
]
