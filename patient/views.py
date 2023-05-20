from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view,permission_classes
from datetime import datetime,date,timedelta,time
from appointment.models import Post,Instruction,Offer,Doctor,Device,Therapist,doctor_appointment,device_appointment
from account.models import Patient
from account.models import PatientProfile
import json
import calendar
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from appointment.views import get_competent_days_in_week,daterange,get_competent_schedule_in_day,get_available_competent_appointments_in_month
#-----------------------------------------------------------
################## HELP FUNCTIONS ##########################
#-----------------------------------------------------------
def date_sorting(list):
     return list['pd']
#-----------------------------------------------------------
def time_duration(publish_date):
    now = datetime.now()
    
#     print(type(now) )
#     print(type(publish_date))
    new_format = '%Y-%m-%d %H:%M:%S'
    pd = datetime.strptime(publish_date,new_format)
    print(pd)
    diff =  now - pd
    timedelta = int(diff.seconds)
    if diff.days >= 1:
          return 'since one day or more'
    if timedelta < 60:
         return str(diff.seconds)+' seconds ago'
    elif timedelta >= 60 and timedelta < 3600:
         mins = round(timedelta/60)
         return str(mins)+' minutes ago '
    elif timedelta >= 3600:
         return str(round(timedelta/3600))+' hours ago'

    return publish_date  
#-----------------------------------------------------------
def get_posts():
    all_posts = Post.objects.all()
    posts = []
    for post in all_posts:
         element = {
              'description':desc_lines(post.description),
              'image':post.photo.url if post.photo else '-',
              'publish_date':time_duration(post.publish_date.strftime('%Y-%m-%d %H:%M:%S')),
               'pd': str(post.publish_date)
         }
         posts.append(element)
    posts.sort(key=date_sorting,reverse=True)  
    return posts     
#-----------------------------------------------------------
def get_instructions():
    all_instructions = Instruction.objects.all()
    instructions = []
    for ins in all_instructions:
         element = {
              'description':desc_lines(ins.description),
              'image':ins.photo.url,
         }
         instructions.append(element)
    instructions.sort(reverse=True)
    return instructions
#----------------------------------------------------------
def dicount(old,new):
     disc =  int((1-new/old)*100)
     return str(disc) + ' %'
#----------------------------------------------------------
def desc_lines(description):
    
     return description.split('\n')
#----------------------------------------------------------     
def get_offers():
    today = timezone.now()
    all_offers = Offer.objects.all()
    offers = []
    for offer in all_offers:
     #     print(offer.ending_date)
     #     print(today)
     #     if offer.ending_date <= today:
               element = {
                    'name':offer.name ,
                    'description':desc_lines(offer.description),
                    'image':offer.photo.url if offer.photo  is not None else '-',
                    'start_date':offer.publish_date.strftime('%Y-%m-%d %H:%M') if offer.publish_date is not None else  '-',
                    
                    'end_date':offer.ending_date.strftime('%Y-%m-%d %H:%M') if offer.ending_date is not None else  '-',
                    'old_price':str(offer.old_price) if offer.old_price is not None else '-',
                    'new_price':str(offer.new_price) if offer.new_price is not None else '-',
                    'discount': str(offer.discount) if offer.discount is not None else '-',
                    'pd': str(offer.publish_date)
               }
        
               offers.append(element)
    offers.sort(key=date_sorting,reverse=True)  
    return offers 
#----------------------------------------------------------
def get_competent_schedule_in_month(name,is_doctor):
     competent_days_in_week = get_competent_days_in_week(name,is_doctor)   
     start_date = date.today()
     end_date = start_date  + timedelta(days=30)
     monthly_presence =[]
     for day in daterange(start_date, end_date):     
          if calendar.day_name[day.weekday()] in competent_days_in_week:
               all_appointments = get_competent_appointments_in_day(name,is_doctor,day)
               day_presence = {
                    'weekDay':calendar.day_name[day.weekday()],
                    'day': day.strftime("%Y-%m-%d"),
                    'timeList':all_appointments,
                     
               }
               monthly_presence.append(day_presence)

     return monthly_presence
#----------------------------------------------------------
def get_competent_appointments_in_day(name,is_doctor,date):
     appointment_list = get_competent_schedule_in_day(name,is_doctor)
     if is_doctor:
          doctor = Doctor.objects.get(name=name)
          reserved_appointment = doctor_appointment.objects.filter(doctor= doctor,date= date)     
     else:
          therapist = Therapist.objects.get(name=name)
          reserved_appointment = device_appointment.objects.filter(therapist=therapist,date=date)
     appointments_details = []     
     for appointment in appointment_list:
          x = {
               'time':appointment[0:-3],
               'free':True
                    }
          for appoi in reserved_appointment :
               if appointment == appoi.time.strftime("%H:%M:%S"): 
                    x['free'] = False
          appointments_details.append(x)     

     return appointments_details


#----------------------------------------------------------
######################## API S ############################
#----------------------------------------------------------
#  API s
@api_view(['POST'])
def get_doctor_image(request):
     body_unicode = request.body.decode('utf-8')
     body = json.loads(body_unicode)
     doctor_name = body['name']
     doctor = Doctor.objects.get(name=doctor_name)
     return JsonResponse({
          'image':doctor.photo.url,
     })
#---------------------------------------------------------
############# API TO GET POSTS AND INSTR #################
#---------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def home_page(request):
     try:
         result = 'invalid'
         user = request.user
         if user.role != 'PATIENT':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
         all_posts = get_posts()
         all_intructions = get_instructions()
         result = 'ok'
         return JsonResponse({
              'result': result,
              'posts':all_posts,
              'posts_length':all_posts.__len__(),
              'ins_length':all_intructions.__len__(),
              'instructions':all_intructions
         })
     except:
          return JsonResponse({
               'result':result,
               'messasge':'invalid data',
          })
#---------------------------------------------------------
############### API FOR GET OFFERS #######################
#---------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def offers(request):
     try:
         result = 'invalid'
         user = request.user
         if user.role != 'PATIENT':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
         all_offers = get_offers()
         result = 'ok'
         return JsonResponse({
              'result':result,
              'offers':all_offers
         })
     except:
           return JsonResponse({
               'result':result,
               'messasge':'invalid data',
          })
#----------------------------------------------------------
############## API FOR PATIENT PROFILE ####################
#----------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def profile_info(request):
     try:
         result = 'invalid'
         user = request.user
         if user.role != 'PATIENT':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
         profile = PatientProfile.objects.get(user=user)
         username = user.username
         bdate = profile.birth_date
         phone_number = profile.phone_number
         relationship = 'Single'  if profile.relationship == 'S' else 'Married'
         picture = profile.img.url
         result ='ok'
         return JsonResponse({
              'result':result,
              'username':username,
              'birth_date' : bdate,
              'phoneNumber':phone_number,
              'relationship':relationship,
              'profilePicture':picture,

         })

     except:
          return JsonResponse({
               'result':result,
               'message' : 'invalid data'
          })
#----------------------------------------------------------
############## API FOR DOCTOR INFO  #######################
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def doctor_info(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'PATIENT':
               return JsonResponse({
                      'result':result,
                      'message':'you don\'t have permission to do this action'
              })
          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          doctor_name = body['doctorName']
          doctor = Doctor.objects.get(name=doctor_name)
          spez = doctor.specialization if doctor.specialization is not None else '-'
          description = doctor.description if doctor.description is not None else '-'
          img = doctor.photo.url
          result = 'ok'
          return JsonResponse({
               'result':result,
               'name':doctor_name,
               'specialization':spez,
               'descriptipn':desc_lines(description),
               'image' : img,
          })
     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : str(e)
          })
#----------------------------------------------------------
########### API FOR GET DOCTOR SCHEDUALE  #################
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def doctor_schedule(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'PATIENT':
               return JsonResponse({
                      'result':result,
                      'message':'you don\'t have permission to do this action'
              })

          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          doctor_name = body['doctorName']
          schedule = get_competent_schedule_in_month(doctor_name,True)
          result = 'ok'
          return JsonResponse({
               'result':result,
               'schedule':schedule
          })
     except :
          return JsonResponse({
               'result':result,
               'message' : 'invalid data'
          })     
#---------------------------------------------------------------------
################## API FOR RESERVE DOCTOR APPOINTMENT ################
#---------------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reserve_doctor_appointment(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'PATIENT':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })
          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          patient_name = user.username
          doctor_name = body['doctorName']
          appointment_date = body['appointmentDate'] 
          appointment_time = body['appointmentTime'] +':00'
          patient = Patient.objects.get(username=patient_name)
          doctor = Doctor.objects.get(name=doctor_name)
          doctor_appointments = doctor_appointment.objects.filter(date=appointment_date,time=appointment_time,doctor=doctor).exists()
          patient_appointments = doctor_appointment.objects.filter(date=appointment_date,time=appointment_time,patient=patient).exists() or  device_appointment.objects.filter(date=appointment_date,time=appointment_time,patient=patient).exists()
          if not patient_appointments:
               if not doctor_appointments:
                    available_appointments = get_available_competent_appointments_in_month(doctor_name,True)
                    for appoint in available_appointments:
                         if appointment_date == appoint['date'] :
                              if appointment_time in appoint['availableAppointments']:
                                   appointment = doctor_appointment()
                                   appointment.doctor = doctor
                                   appointment.patient = patient
                                   appointment.date = appointment_date
                                   appointment.time = appointment_time
                                   appointment.save()
                                   result='ok'
                                   return JsonResponse({
                                        'result':result,
                                        'message':'appointment added successfuly',
                                   })
                              
                              else:
                                   return JsonResponse({
                                        'result':result,
                                        'message':'doctor is not available in this time',
                                   })
                    return JsonResponse({
                                        'result':result,
                                        'message':'Doctor is not available in this time',
                                        })           
               else:
                    return JsonResponse({
                         'result':result,
                         'messagee':'Doctor  have an appointment in '+str(appointment_date)+' at  '+str(appointment_time)+' oclock already ',
               })                    
          else:
               return JsonResponse({
                    'result':result,
                    'messagee':'You   have an appointment in '+str(appointment_date)+' at  '+str(appointment_time)+' oclock already ',
               })
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid data'
          })
#---------------------------------------------------------------------
################## API FOR RESERVE DOCTOR APPOINTMENT ################
#---------------------------------------------------------------------                   
     