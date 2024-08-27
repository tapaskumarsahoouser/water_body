from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models 
from django.contrib.gis.geos import Point
from django.db import models as django_models
import datetime

class Admin(models.Model):
    Name = models.CharField(max_length=20)
    Mob=models.BigIntegerField(primary_key=True,unique=True)
    Email=models.EmailField()
    password = models.CharField(max_length=50, blank=True, null=True)
    avtar = models.ImageField(upload_to='avtar/',default='avtar/avtar.png')

    def __str__(self):
        return str(self.Name)
    
    
class User(models.Model):                                               
    Name=models.CharField(max_length=20)
    Mob=models.BigIntegerField(primary_key=True,unique=True)
    Email=models.EmailField()
    password = models.CharField(max_length=50, blank=True, null=True)
    adhaar=models.CharField(max_length=16, blank=True, null=True)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    avtar = models.ImageField(upload_to='avtar/',default='avtar/avtar.png')
    user_category = models.CharField(max_length=20, blank=True, null=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.Name)
    
    
class Pond(models.Model):
    name = models.CharField(max_length=50)
    latlong = models.CharField(max_length=50)
    location = models.GeometryField(unique=True,null=True,blank=True)
    area = models.CharField(max_length=50, blank=True,null=True)
    city = models.CharField(max_length=50)
    telegram_group_id = models.CharField(max_length=100, null=True,blank=True) 
    registration = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name)