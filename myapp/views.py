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
from django.middleware.csrf import get_token




@csrf_exempt
def registration(request):
    if request.method == 'POST':
        regd_instance=JSONParser().parse(request)
        firstname=regd_instance.get('firstname')
        lastname=regd_instance.get('lastname')
        email=regd_instance.get('email')
        mobno=regd_instance.get('mobno')
        adhaar=regd_instance.get('adhaar')
        user_cat=regd_instance.get('user_cat')
        password=regd_instance.get('params')
        fullname=firstname+" "+lastname
        instance=User.objects.filter(Mob=mobno)
        
        try:
            if not instance.exists():
                token = get_token(request)
                datas = User(Name=fullname,Email=email,Mob=mobno,password=password,adhaar=adhaar,user_category=user_cat,reset_token=token)
                datas.save()
                return JsonResponse({"massage":"Registration Successfull"})
            else:
                return JsonResponse({"massage":"User Mobile number already registered, Report to Admin"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        
# from .backends import CustomBackend
import time

# Define a dictionary to keep track of login attempts  
login_attempts = {}

@csrf_exempt
def login(request):
    if request.method == 'POST':
        userdata = JSONParser().parse(request)
        identifier = userdata.get('identifier')
        password = userdata.get('password')

        def is_valid_email(identifier):
            return "@" in identifier

        try:
            if is_valid_email(identifier):
                admins = Admin.objects.filter(Email=identifier, password=password)
            else:
                admins = Admin.objects.filter(Mob=identifier, password=password)

            if admins.exists():
                csrf_token = csrf.get_token(request)
                admin = admins.first()
                response_data = {
                    'message': 'You are successfully entered the admin page...',
                    'Mob': admin.Mob,
                    'name': admin.Name,
                    'password': password,
                    'email': admin.Email,
                    'csrf_token': csrf_token
                }
                return JsonResponse(response_data, status=200)

        except ObjectDoesNotExist:
            pass

        try:
            if is_valid_email(identifier):
                users = User.objects.filter(Email=identifier, password=password)
            else:
                users = User.objects.filter(Mob=identifier, password=password)

            if users.exists():
                user = users.first()
                response_data = {
                    'message': 'You are successfully logged in...',
                    'Mob': user.Mob,
                    'name': user.Name,
                    'email': user.Email
                }
                return JsonResponse(response_data, status=200)

        except ObjectDoesNotExist:
            pass

        return JsonResponse({'message': 'Invalid credentials'}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=400)




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

from django.db.models import Count

csrf_exempt
def viewuser(request):
    # print(mob)
    if request.method == 'GET':
        # if not mob:
        #     return JsonResponse({"error": "Mobile number not provided"})

        # if not User.objects.filter(Mob=mob):
        #     return JsonResponse({"error": "Mobile number not found"})
        
        users = User.objects.all()
        data = []

        for user in users:
            pond_count = 0
            
            pond_count += Pond.objects.filter(registration=user).count()

            user_data = {
                'name': user.Name,
                'email': user.Email,
                'mob': user.Mob,
                'password': user.password,
                'pond_count': pond_count
            }
            data.append(user_data)

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)



@csrf_exempt
def pondcount(request, registration_id):
    if request.method == 'GET':
        value = Cluster.objects.get(id=registration_id)
        result = Pond.objects.filter(registration_id=value) \
            .values('registration_id') \
            .annotate(num_ponds=Count('id')) \
            .values('num_ponds')  

        if result:
            return JsonResponse({'pond_counts': list(result)})
        else:
            return JsonResponse({'message': 'No pond locations found for the given registration ID'}, status=404)



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
            user = User.objects.all()
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
        
        
        
import redis
from django.conf import settings

def get_redis_connection():
   try:
       return redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0,password=settings.REDIS_PASSWORD, ssl=True)
   except redis.ConnectionError as e:
       print(f"Redis connection error: {e}")
       return None

@csrf_exempt
def work_assign(request):
   if request.method == 'POST':
       jsondata = JSONParser().parse(request)
       all_tasks = jsondata.get('tasks')
       print(all_tasks)
       r = get_redis_connection()
       if r is None:
           return JsonResponse({"error": "Unable to connect to Redis"}, status=500)
       
       for i in all_tasks:
           try:
               task_instance = Task_Category.objects.get(name=i[0])
               pond_instance = Pond.objects.get(id=i[5])
               worker_instance = Worker_details.objects.get(name=i[3])
               
               # Prepare the task details for Redis
               task_id = Task.objects.create(
                   name=task_instance,
                   date=datetime.datetime.now().strftime("%Y-%m-%d"),
                   from_time=i[1],
                   to_time=i[2],
                   worker_name=worker_instance,
                   feed_weight=i[4],   
                   pond_id=pond_instance,
               )
               task_data = {
                   'category_name': task_instance.name,  # Use the name attribute here
                   'option1': "Yes",
                   'option2': "No",
                   'feed_weight': i[4],
                   'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                   'from_time': i[1],
                   'to_time': i[2],
                   'pond_id': pond_instance.id,  # Use the ID attribute here
                   'group_id': pond_instance.telegram_group_id,
                   'worker_name': worker_instance.name,  # Use the name attribute here
                   'task_id': task_id.id,
               }

               # Ensure all values are converted to strings before storing in Redis
               task_data = {key: str(value) for key, value in task_data.items()}

               # Store the task details in a hash
               task_key = f"task:{datetime.datetime.now().strftime('%H:%M:%S.%f')}"
               r.hset(task_key, mapping=task_data)
               # Set the expiration time to 86400 seconds (1 day)
               r.expire(task_key, 86400)
               print(f"Task data prepared: {task_data}")
               


           except Exception as e:
               return JsonResponse({"error": str(e)}, status=500)

   return JsonResponse({"message": "Task dataset stored in both database & Redis"})
       
@csrf_exempt
def category(request):
   if request.method == 'GET':
       try:
           result = Task_Category.objects.all()
           response = []
           for i in result:
               response.append({
                   "name" : i.name
               })
           return JsonResponse({'category':response}, safe=False)
       except:
           return JsonResponse({'category':'error'})

   
@csrf_exempt
def workerview(request,mob):
   if request.method == 'GET':
       try:
           user = User.objects.get(Mob=mob)
           if user:
               result = Worker_details.objects.all()
               response = []
               for i in result:
                   response.append({
                       "name":i.name
                   })
               return JsonResponse({'Employee':response}, safe=False)
       except:
           return JsonResponse({'category':'error'})


@csrf_exempt
def userpondsid(request, id):
    if request.method == 'GET':
        try:
            pond = Pond.objects.get(id=id)
            instance = ServicePayment.objects.filter(pond_id=pond)

            response_data = {
            'id': pond.id,
            'name': pond.name,
            'city':pond.city,
            'location': pond.location.coords,
            'area':pond.area,
            'payments': []
        }
            for i in instance:
                payment_info = {    
                    i.service_name: i.token
                }
                response_data['payments'].append(payment_info)

            return JsonResponse(response_data)
            
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Pond location not found'}, status=404)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
    
    

@csrf_exempt
def graph(request, id):
    if request.method == 'POST':
        try:
            jsondata = JSONParser().parse(request)
            month = jsondata.get('month')

            # Debugging statement, should be removed or handled in a proper logging mechanism in production
            print(month)

            if not month:
                return JsonResponse({'message': 'Month is required'}, status=400)

            # Assuming Parameter model has the fields `pond` and `created_at`
            temp = Parameter.objects.filter(
                pond=id,
                created_at__month=month
            ).order_by('-created_at')[:5]

            if temp.exists():
                ph_values = [param.pH for param in temp]
                # Uncomment and define other values if needed
                # DO_values = [param.dissolved_oxygen for param in temp]
                # ndvi_values = [param.NDVI for param in temp]
                # ndti_values = [param.NDTI for param in temp]
                # gci_values = [param.GCI for param in temp]
                # ndci_values = [param.NDCI for param in temp]
                # ndwi_values = [param.NDWI for param in temp]
                # TSS_values = [param.TSS for param in temp]
                # cdom_values = [param.CDOM for param in temp]
                AQUATIC_MACROPYTES_values = [param.AQUATIC_MACROPYTES for param in temp]

                # Calculate weeks based on `created_at` day of the month
                weeks = [f"week {(i.created_at.day - 1) // 7 + 1}" for i in temp]
                weeks.reverse()

                response = {
                    'ph': ph_values,
                    # 'dissolved_oxygen': DO_values,
                    # 'NDVI': ndvi_values,
                    # 'NDTI': ndti_values,
                    # 'GCI': gci_values,
                    # 'NDCI': ndci_values,
                    # 'NDWI': ndwi_values,
                    # 'TSS': TSS_values,
                    # 'CDOM': cdom_values,
                    'AQUATIC_MACROPYTES': AQUATIC_MACROPYTES_values,
                    'week': weeks
                }
                return JsonResponse(response, safe=False)
            else:
                return JsonResponse({'message': 'No data found for the given month and pond'}, status=404)

        except Exception as e:
            # Catching broad exceptions is generally not recommended, but it ensures something is returned
            return JsonResponse({'message': 'An error occurred', 'error': str(e)}, status=500)
        
    # Handle methods other than POST
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def demo(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            jsondata = JSONParser().parse(request)
            name = jsondata.get('name')
            latitude = jsondata.get('latitude')
            longitude = jsondata.get('longitude')
            polygon_points = jsondata.get('location', None)
            pond_id = jsondata.get('pond_id')  # This is the ID to match
            area = jsondata.get('area')
            city = jsondata.get('city')
            # telegram_group_id = jsondata.get('telegram_group_id')  # Uncomment if needed

            if not pond_id:
                return JsonResponse({'message': 'Pond ID is required'}, status=400)

            # Fetch the Pond instance using the pond_id
            try:
                pond_instance = Pond.objects.get(id=pond_id)
            except Pond.DoesNotExist:
                return JsonResponse({'message': 'Pond not found for the given ID'}, status=404)

            # Update the Pond instance
            pond_instance.name = name
            pond_instance.city = city
            pond_instance.area = area

            # Handle polygon points
            if polygon_points:
                points_str = ', '.join([f'{point[0]} {point[1]}' for point in polygon_points])
                points_str += f', {polygon_points[0][0]} {polygon_points[0][1]}'  # Closing the polygon
                pond_instance.location = f'POLYGON(({points_str}))'
            else:
                pond_instance.location = None

            # Set latitude and longitude
            latitude_str = str(latitude)
            longitude_str = str(longitude)
            pond_instance.latlong = f'({latitude_str},{longitude_str})'

            # Save the updated Pond instance
            pond_instance.save()

            return JsonResponse({'message': 'Location updated successfully.'})

        except ValueError as ve:
            return JsonResponse({'message': 'Invalid data format', 'error': str(ve)}, status=400)

        except Exception as e:
            return JsonResponse({'message': 'Location not updated', 'error': str(e)}, status=500)

    return JsonResponse({'message': 'Method not allowed'}, status=405)



@csrf_exempt
def deleteuser(request,mob):
    if request.method == 'DELETE':    
        # if not admin_mob:
        #     return JsonResponse({"error": "admin mobile number not provided"})
        # if not Super.objects.filter(Mob=admin_mob):
        #     return JsonResponse({"error": "admin mobile number not found"})
            
        try:
            print("jhfjhgi")
            var = User.objects.get(Mob=mob)
            print(var)
            var.delete()
            print("jijh")
            return JsonResponse({'message':'user delete successfull'})
        except:
            return JsonResponse({'message':'user Already deleted'})
    else:
        return JsonResponse({'message':'Invalid user'})