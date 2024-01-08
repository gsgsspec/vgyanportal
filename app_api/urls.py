from django.urls import path
from app_api import views

urlpatterns = [
    path('add-user',views.addUser),
    path('login',views.loginView),
    path('save-profile',views.saveProfile),
    path('save-rating',views.saveRating),

    path('get-module-lessons',views.getModuleLesson),
    path('save-question',views.saveQuestion),
    path('get-questions',views.getQuestion),
    path('get-lesson-video',views.getlessonVideoDetails),
    path('save-assessment',views.saveAssessmentDetails),
    path('update-assessment-status',views.updateAssessmentDetails),
    path('save-video-activity',views.saveVideoActivity),
    path('vgyan-cors-mod-les-name',views.courseModuleName),
    path('assessmentslist',views.assessmentslist),
    path('all-notifications',views.allNotifications),
    path('remove-notification',views.removeNotification),
    path('mark-as-read-notifications',views.markAsReadNotification),
    path('Check-latest-notifications',views.checkLatestNotifications),
    path('update-lesson-status',views.updateLessonStatus)
]
