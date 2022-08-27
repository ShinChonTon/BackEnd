from xml.etree.ElementInclude import include
from django.urls import path

from .views import LoginView, SignUpView, LocationView, MeetingsAPI,MeetingAPI

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('meetings/',MeetingsAPI.as_view()),
    path('meeting/ <int:meeting_id>',MeetingAPI.as_view()),
    path('location/', LocationView.as_view()),
]
