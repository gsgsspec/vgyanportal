from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginPage),
    path('courses',views.coursesPage),
    path('profile',views.profilePage),
    path('course/question',views.askQuestionPage),
    path('rating',views.ratingPage),
    path('course-details/<int:cid>',views.courseDetailsPage),
    path('assessments',views.assessmentsPage),
]
