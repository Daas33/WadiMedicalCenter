from django.urls import path
from . import views
from django.contrib import auth
from .models import Patient
import json
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .views import Registeration
class CustomAuthToken(ObtainAuthToken):

     def post(self, request, *args, **kwargs):
        try:
            result = 'invalid'
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode) 
            username = body['username']
            password = body['password']
            
            if Patient.patient.filter(username = username).exists():
                user = auth.authenticate(username=username, password = password)
                if user is not None:
                    auth.login(request,user)
                    token = Token.objects.get(user=user).key
                
                    result = 'ok'
                    return JsonResponse({
                        'result':result,
                        'username':user.username,
                        'token':token,
                        
                    })
                else:
                    return JsonResponse({
                        'result':result,
                        'message':'password incorrect'
                    })

                
            else:
                result = 'invalid'
                return JsonResponse({
                    'result':result,
                    'message':'you are not registerd'
                })      
        except:
                
                return JsonResponse({
                    'result':result,
                    'message':'invalid data'
                })
        
class CustomAuthTokenEmployee(ObtainAuthToken):

     
     def post(self, request, *args, **kwargs):
                body_unicode = request.body.decode('utf-8')
                body = json.loads(body_unicode)
                username = None
                password  =None
                role = None
                result = 'invalid'
                try:
                    username = body['username']
                    password = body['password']
                    user = auth.authenticate(username=username, password = password)
                    
                    if user is not None:
                        auth.login(request, user)
                        token = Token.objects.get(user=user).key
                        role = user.role
                        result = 'ok'
                       
                        return JsonResponse({
                            'result':result,
                            'role':role,
                            'token':token,

                        })
                    else:
                        return JsonResponse({'result':'invalid',
                                        'message' : 'username or password maybe incorrect'})


                    
                except:
                    return JsonResponse({'result':'invalid',
                                        'message' : 'invalid data'})


urlpatterns=[
    path('',views.default),
    path('employee_login',CustomAuthTokenEmployee.as_view(), name='employee_login'),
    path('signup',views.Registeration.as_view(),name='signup'),
    # path('patient_login',views.patient_login,name='patient_login'),
    path('patient_login', CustomAuthToken.as_view(),name='login'),
   
    # path('logout',views.logout,name='logout'),
]