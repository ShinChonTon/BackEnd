from asyncio.windows_events import NULL
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404

from .serializer import MeetingSerializer, UserSerializer, LocationSerializer
from .models import Meeting, User, Location

from .serializer import UserLoginSerializer, UserSerializer
from .serializer import LocationSerializer

from .models import Location
from .serializer import LocationSerializer

# Create your views here.

class SignUpView(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'회원가입 성공', 'data':serializer.data})
        return Response({'message':'회원가입 실패', 'error':serializer.errors})

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message":"로그인 성공", 'data':serializer.data})
        return Response({"message":"로그인 실패", 'error':serializer.errors})


class LocationView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

class  MeetingsAPI(APIView):  # 미팅 전체
    
    def get(self,request):          # 미팅 정보가져오기
        meetings= Meeting.objects.all()
        serializer = MeetingSerializer(meetings,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request): # request에 카테고리도 포함하여 포스트    # 넘겨줘야하는 값(user_id, name, image, category)
        author=get_object_or_404(User,id=request.data.user_id)
        location = Location.objects.get(location1=request.data.location1,location2=request.data.location2,location3=request.data.location3,location4=request.data.location4)
        serializer = MeetingSerializer(data= request.data,author=author,participant=author, location= location)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class  MeetingAPI(APIView): 
    
    def put(self, request, meeting_id):# 글 수정
        meeting=get_object_or_404(Meeting,id=meeting_id)
        serializer = MeetingSerializer(meeting, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, meeting_id):# 글 삭제
        meeting=get_object_or_404(Meeting,id=meeting_id)
        meeting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
