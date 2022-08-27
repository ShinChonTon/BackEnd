from operator import mod
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class Location(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    si = models.CharField(max_length=10, default='')
    gu = models.CharField(max_length=10, default='')
    dong = models.CharField(max_length=10, default='')
    detail_loc = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()

class User(AbstractUser):
    id = models.CharField(max_length=15, unique=True, default='', primary_key=True)
    nickname = models.CharField(max_length=15, unique=True, default='')
    birth = models.DateField(null=True)
    def __str__(self):
        return self.username


class Location(models.Model):
    location1 = models.CharField(max_length=100)
    location2 = models.CharField(max_length=100)
    location3 = models.CharField(max_length=100)
    location4 = models.CharField(max_length=100)
    location5 = models.CharField(max_length=100)
    location6 = models.CharField(max_length=100)
    
    # @receiver(post_save, sender=Meeting)
    # def create_festival_optioncount(sender, instance, created, **kwargs):
    #     if created:
    #           Location.objects.create(meeting=instance)    
    

class Meeting(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meeting_author')
    location = models.ForeignKey(Location,null=True,on_delete=models.SET_NULL, related_name='meeting_location')
    participant = models.ManyToManyField(User,  related_name='meeting_participant', blank=True)
    name = models.CharField(max_length=300)
    body = models.CharField(max_length=600)
    max_people = models.IntegerField(null=True)
    plan_date = models.DateTimeField( blank= True)
    create_date = models.DateTimeField(auto_now_add= True)
    thema = models.CharField(max_length=20,blank= True) # 운동, 영화, 등등
    age = models.CharField(max_length=100) # 20대. 30대, 전연령
    
 
    def __str__(self):
        return self.name
