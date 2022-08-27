from asyncio.windows_events import NULL
from unicodedata import name
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
import requests

from .serializer import MeetingSerializer, UserSerializer, LocationSerializer,UserLoginSerializer
from .models import Meeting, User, Location
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
    
    def post(self,request): # request에 카테고리도 포함하여 포스트    # 넘겨줘야하는 값(user_id, name, body, address, max_people, plan_date , thema, age)
        author=get_object_or_404(User,id=request.data.user_id)
        if Location.objects.filter(address=request.data.address).exists():
            location=get_object_or_404(Location,address=request.data.address)
        else :
            url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
            params = {'query': request.data.address, 'analyze_type':'exact'}
            headers = {"Authorization": "KakaoAK bcc331e79192b044188e99f15b75dd78"}
            x = requests.get(url, params=params, headers=headers).json()['documents'][0]['x']
            y = requests.get(url, params=params, headers=headers).json()['documents'][0]['y']
            location_serializer = LocationSerializer(address=request.data.address, latitude = x, longitude = y)
            location_serializer.save()
            location=get_object_or_404(Location,address=request.data.address)
            
        serializer = MeetingSerializer(author=author,location= location,participant=author,name= request.data.name ,body=request.data.body,max_people=request.data.max_people,plan_date=request.data.plan_date,thema=request.data.thema,age=request.data.age)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meeting_author')
    # location = models.ForeignKey(Location,null=True,on_delete=models.SET_NULL, related_name='meeting_location')
    # participant = models.ManyToManyField(User,  related_name='meeting_participant', blank=True)
    # name = models.CharField(max_length=300)
    # body = models.CharField(max_length=600)
    # max_people = models.IntegerField(null=True)
    # plan_date = models.DateTimeField( blank= True)
    # create_date = models.DateTimeField(auto_now_add= True)
    # thema = models.CharField(max_length=20,blank= True) # 운동, 영화, 등등
    # age = models.CharField(max_length=100) # 20대. 30대, 전연령

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
