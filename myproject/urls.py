from django.contrib import admin
from django.urls import path,include
from myapp import views
from myapp.views import *
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('common_login/',views.common_login),
    path('userpond_view/<Mob>/',views.userpond_view),
    path('adminpond_view/<Mob>/',views.adminpond_view),

]
