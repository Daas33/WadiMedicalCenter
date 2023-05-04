from django.shortcuts import render , redirect
from rest_framework.decorators import api_view,permission_classes
from django.contrib import auth
import json 
from django.http import HttpResponse, JsonResponse
from .models import Patient,PatientProfile,User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.files.base import ContentFile
import base64

#--------------------------------------------------------------------------------
# ############################# employee login ################################

@api_view(['POST'])
def employee_login(request):
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
        # user = Usert.objects.get(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            result = 'ok'
            role = user.role
            return JsonResponse({
                'result':result,
                'role':role

            })
        else:
            return JsonResponse({'result':'invalid',
                              'message' : 'username or password maybe correct'})


        
    except:
        return JsonResponse({'result':'invalid',
                              'message' : 'username or password maybe correct'})
#--------------------------------------------------------------------------------
# ############################# sign up Patients ################################
    
@api_view(['POST'])
# @csrf_exempt
def signup(request):
    try:
         result = 'invalid'
         body_unicode = request.body.decode('utf-8')
         body = json.loads(body_unicode)  
         username = body['username']
         password = body['password']
         # value 1 if is female and any else if male
         gender = 'F' if body['gender'] == '1'  else 'M'

        #  #value 1 if is Single and any else if married
         relationship = 'S' if  body['relationship'] == '1' else 'M'
         phone_number  = body['phoneNumber']
         bdate =body['birthDate']
        #  profile_picture = body['profile_picture']
        #  profile_picture.replace('data:image/png;base64,', '')
         if Patient.objects.filter(username=username).exists():
              return JsonResponse({
                  'result':result,
                  'message':'the user already exists'
              })
         else:
             #add user
          print('1')
          user = Patient.objects.create_user(
                 username = username,
                 password  = password,  
                                            ) 
          print('2') 
          
          user.save()
          profile = PatientProfile.objects.get(user=user)
          profile.gender = gender
          profile.relationship = relationship
          profile.phone_number = phone_number
          profile.birth_date = bdate
        #   profile.img = profile_picture
          profile.save()
          token = Token.objects.get(user=user).key

          result = 'ok'

         return JsonResponse({
                'result':result,
                'message':'sucsses patient has been registered',
                'token':token,
            })

        #img
        #finger_print
        
    except:
        return JsonResponse({
            'result':result,
            'message':'invalid data'
        })
     
#---------------------------------------------------------------------------------
################################ patient login ###################################
@api_view(['POST'])
def patient_login(request):
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
                    'username':username,
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
#---------------------------------------------------------------------------------
################################ logout ##########################################
# @api_view(['POST'])
# def logout(request):
#      if auth.logout(request):
#          return JsonResponse({'result':'ok'})
#---------------------------------------------------------------------------------
################################ forget password #################################
class Registeration(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
       
        try:
            result = 'invalid'
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)  
            username = body['username']
            password = body['password']
            # value 1 if is female and any else if male
            gender = 'F' if body['gender'] == '1'  else 'M'

            #  #value 1 if is Single and any else if married
            relationship = 'S' if  body['relationship'] == '1' else 'M'
            phone_number  = body['phoneNumber']
            bdate =body['birthDate']
            profile_picture = body['profile_picture']
            # profile_picture.replace('data:image/jpeg;base64,', '')
            if Patient.objects.filter(username=username).exists():
                return JsonResponse({
                    'result':result,
                    'message':'the user already exists'
                })
            else:
             
                user = Patient.objects.create_user(
                        username = username,
                        password  = password,  
                                                    ) 
               
                
                user.save()
                profile = PatientProfile.objects.get(user=user)
                profile.gender = gender
                profile.relationship = relationship
                profile.phone_number = phone_number
                profile.birth_date = bdate
                
                format, imgstr = profile_picture.split(';base64,') 
                ext = format.split('/')[-1] 
                patient_img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                profile.img = patient_img
                profile.save()
                token = Token.objects.get(user=user).key

                result = 'ok'

                return JsonResponse({
                        'result':result,
                        'message':'sucsses patient has been registered',
                        'token':token,
                    })

            #img
            #finger_print
            
        except:
            return JsonResponse({
                'result':result,
                'message':'invalid data'
            })
      
#---------------------------------------------------------------------------------
########################## default LOGO ##########################################
def default(request):
     return render( request,'index.html') 
