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

@admin.register(Worker_details)
class Worker_details(admin.GISModelAdmin):
    list_display = ['mobno','name','user']


@admin.register(Task_Category)
class Task_Category(admin.GISModelAdmin):
    list_display = ['name']


@admin.register(Task)
class Task(admin.GISModelAdmin):
    list_display = ['name','option1','option2','feed_weight','date','from_time','to_time','pond_id','worker_name']
    
    
@admin.register(ServicePayment)
class ServicePayment(admin.ModelAdmin):
    list_display = ('user_name', 'pond_id', 'service_name', 'amount', 'order_id', 'token', 'created_at')

