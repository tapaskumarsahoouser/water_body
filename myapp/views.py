from django.shortcuts import render
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from rest_framework.parsers import JSONParser
from django.contrib.gis.measure import D
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def common_login(request):
    try:
        jsondata = JSONParser().parse(request)
        Mob = jsondata.get('Mob')

        if not Mob:
            return JsonResponse({'message': 'Mobile number is required'}, status=400)

        try:
            user = User.objects.get(Mob=Mob)
            response_data = {
                'Mob': user.Mob,
                'name': user.Name,
                'email': user.Email,
                'cat': 'user'
            }
            return JsonResponse(response_data, safe=False)
        except User.DoesNotExist:
            admin = Admin.objects.filter(Mob=Mob).first()
            if admin:
                return JsonResponse({'cat': 'admin','Mob':admin.Mob}, safe=False)
            else:
                return JsonResponse({'message': 'User not found'}, status=404)

    except Exception as e:
        return JsonResponse({'message': f'Error: {str(e)}'}, status=400)


@csrf_exempt
def userpond_view(request,Mob):
    if request.method == 'GET':
        try:
            value = User.objects.get(Mob=Mob)
            pond = Pond.objects.filter(registration=value)
            data = []
            for i in pond:
                vv ={
                    "id":i.id,
                    "name":i.name,
                    "latlong":i.latlong,
                    "location":i.location.coords,
                    "Area":i.area,
                    "city":i.city,
                }
                data.append(vv)
            return JsonResponse(data, safe=False)

        except:
            return JsonResponse({'message':'error'},status=400)
 

@csrf_exempt
def adminpond_view(request, Mob):
    if request.method == 'GET':
        try:
            admin = Admin.objects.get(Mob=Mob)
            user = User.objects.filter(admin=admin)
            pond = Pond.objects.filter(registration__in=user)  

            data = []
            for i in pond:
                vv = {
                    "id": i.id,
                    "name": i.name,
                    "latlong": i.latlong,
                    "location": i.location.coords,
                    "Area": i.area,
                    "city": i.city,
                }
                data.append(vv)
            
            return JsonResponse(data, safe=False)

        except Admin.DoesNotExist:
            return JsonResponse({'message': 'Admin not found'}, status=404)
        
        except Exception as e:
            return JsonResponse({'message': 'Error', 'details': str(e)}, status=400)