from django.urls import path
from app_api import views


urlpatterns = [
    path('add-user',views.addUser),
    path('login',views.loginView),
    path('save-profile',views.saveProfile),
    path('get-module-lessons',views.getModuleLesson),
    path('save-rating',views.saveRating),

    path('save-question',views.saveQuestion),
    path('get-questions',views.getQuestion),
]
