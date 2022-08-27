from xml.etree.ElementInclude import include
from django.urls import path
<<<<<<< HEAD
from .views import LoginView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
=======
from irion import urls
from .views import MeetingsAPI,MeetingAPI
from .views import LocationView

app_name = 'irion'

urlpatterns = [
    path('meetings/',MeetingsAPI.as_view()),
    path('meeting/ <int:meeting_id>',MeetingAPI.as_view()),
<<<<<<< HEAD
>>>>>>> 619a8f03b537e717f38ddf19437c44cc12f93409
=======
    path('location/', LocationView.as_view()),
>>>>>>> f4a7dd0b13f595d0d6500f37c7d08a4646cc74cd
]
