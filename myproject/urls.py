from django.contrib import admin
from django.urls import path,include
from myapp import views
from myapp.views import *
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.registration),
    path('login/',views.login),
    path('common_login/',views.common_login),
    path('viewuser/',views.viewuser),
    path('pondcount/<registration_id>/',views.pondcount),
    path('userpond_view/<Mob>/',views.userpond_view),
    path('adminpond_view/<Mob>/',views.adminpond_view),
    path('work_assign/',views.work_assign),
    path('category/',views.category),
    path('workerview/<mob>/',views.workerview),
    path('userpondsid/<id>/',views.userpondsid),
    path('graph/<id>/',views.graph),
    path('demo/',views.demo),
    path('deleteuser/<mob>/',views.deleteuser),
    
    
    

]
