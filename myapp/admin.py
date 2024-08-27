from django.contrib import admin
from django.contrib.gis import admin
from .models import *



@admin.register(Admin)
class Admin(admin.ModelAdmin):
    list_display = ['Name','Mob','Email','password','avtar']

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['Name','Mob','Email','password','adhaar','reset_token','avtar','user_category']


@admin.register(Pond)
class Pond(admin.GISModelAdmin):
    list_display = ['id','name','latlong','location','area','city','telegram_group_id','registration']

