from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view,permission_classes
from datetime import datetime,date,timedelta,time
from appointment.models import Post,Instruction,Offer,Doctor,Device,Therapist,doctor_appointment,device_appointment,Section,rate
from account.models import Patient
from account.models import PatientProfile
import json
import calendar
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from appointment.views import get_competent_days_in_week,daterange,get_competent_schedule_in_day,get_available_competent_appointments_in_month
from appointment.views import get_device_reserved_appointments_in_day
from django.core.files.base import ContentFile
import base64
#-----------------------------------------------------------
################## HELP FUNCTIONS ##########################
#-----------------------------------------------------------
def name_sorting(list):
     return list['name']
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

#----------------------------------------------------------
def get_first_day(name,is_doctor):
     if is_doctor:
          doctor = Doctor.objects.get(name=name)
     else:
          therapist = Therapist.objects.get(name=name)
     competent_days_in_week = get_competent_days_in_week(name,is_doctor)            
     for day in daterange(date.today(),date.today()+timedelta(days=6)):

          if calendar.day_name[day.weekday()] in competent_days_in_week:
               return day
     return date.today()
#----------------------------------------------------------
def get_competent_schedule_in_month(name,is_doctor):
     competent_days_in_week = get_competent_days_in_week(name,is_doctor)
     start_date = get_first_day(name,is_doctor)
     print(start_date)
     # date.today()
     end_date = start_date  + timedelta(days=30)
     monthly_presence =[]
     for day in daterange(start_date, end_date):     
          if calendar.day_name[day.weekday()] in competent_days_in_week:
               all_appointments = get_competent_appointments_in_day(name,is_doctor,day)
               day_presence = {
                    # 'weekDay':calendar.day_name[day.weekday()],
                    'day': day.strftime("%Y-%m-%d"),
                    'timeList':all_appointments,
                     
               }
              
          else : 
                day_presence = {
                    # 'weekDay':calendar.day_name[day.weekday()],
                    'day': day.strftime("%Y-%m-%d"),
                    'timeList':None,
                     
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
def switch(appointment : doctor_appointment|device_appointment):
     today = date.today()
     now = datetime.now()
     if appointment.date - today < timedelta(0) : 
          return 'pre'
     elif appointment.date - today == timedelta(0):
          if now > datetime.combine(appointment.date,appointment.time) : 
               return 'pre'
          else:
               return 'upcom'
     else : 
          return 'upcom'     


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
         is_single = True  if profile.relationship == 'S' else False
         is_male = True if profile.gender == 'M' else False
         picture = profile.img.url
         result ='ok'
         return JsonResponse({
              'result':result,
              'username':username,
              'birth_date' : bdate,
              'phoneNumber':phone_number,
              'isSingle':is_single,
              'isMale' : is_male,
              'profilePicture':picture,

         })

     except:
          return JsonResponse({
               'result':result,
               'message' : 'invalid data'
          })
#----------------------------------------------------------
############## API FOR CATEGORIES  ########################
#----------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def categories(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'PATIENT':
               return JsonResponse({
                    'result':result,
                    'message':'you don\'t have permission to do this action'
               })
          devices_in_sections =[]
          doctors_in_sections =[]
          sections = Section.objects.all()
          for section in sections:
               number = Doctor.objects.filter(section=section).count()
               if number > 0:
                    section_object = {
                         'name':section.name,
                         'fullName':section.full_name if section.full_name is not None else  '-',
                         'image':section.photo.url ,
                         'number': number,
                         }
                    doctors_in_sections.append(section_object)
          for section in sections:
               number = Device.objects.filter(section=section).count()
               if number > 0:
                    section_object = {
                    'name':section.name,
                    'fullName':section.full_name if section.full_name is not None else  '-',
                    'image':section.photo.url ,
                    'number': number,
                    }
                    devices_in_sections.append(section_object)
          result= 'ok'
          return  JsonResponse({
               'result':result,
               'doctorsInSections':doctors_in_sections,
               'devicesInSections':devices_in_sections,
          })

     except Exception as e:
           return JsonResponse({
                'result':result,
                'message' : 'invalid data',
             
           })
#-----------------------------------------------------------
############### API FOR SECTION DETAILS ####################
#-----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def doctors_in_section(request):
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
          section_name = body['name']
          section = Section.objects.get(name=section_name)
          doctors_list =[]
          doctors = Doctor.objects.filter(section=section)
          for doctor in doctors:
               doctor_details = {
                    'name':doctor.name,
                    'image':doctor.photo.url,
                    'isDoctor':True,
                    'description':desc_lines(doctor.description)[0],
                    'specialization':doctor.specialization,
               }
               doctors_list.append(doctor_details)
          doctors_list.sort(key=name_sorting)
          result='ok'
          return JsonResponse({
               'result':result,
               'doctorsList':doctors_list,

          })
     except Exception as e:
           return JsonResponse({
                'result':result,

                'message' : 'invalid data',
                'err':str(e),
           })
#----------------------------------------------------------
# get doctor appointments and info
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
               'message' : 'invalid data',
          })
#----------------------------------------------------------
########### API FOR GET DOCTOR SCHEDULE  ##################
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
     except Exception as e :
          return JsonResponse({
               'result':result,
               'message' : 'invalid data',
               'err':str(e)
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
################## API FOR DEVICE SECTION DETAILS ####################
#---------------------------------------------------------------------                   
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def devices_in_section(request):
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
          section_name = body['name']
          section = Section.objects.get(name=section_name)
          devices_list =[]
          devices = Device.objects.filter(section=section)
          for device in devices:
               doctor_details = {
                    'name':device.name,
                    'image':device.photo.url,
                    'isDoctor':False,
                    'description':desc_lines(device.description)[0],
                    
               }
               devices_list.append(doctor_details)
          devices_list.sort(key=name_sorting)
          result='ok'
          return JsonResponse({
               'result':result,
               'devicessList':devices_list,

          })
     except Exception as e:
           return JsonResponse({
                'result':result,

                'message' : 'invalid data',
           })
#----------------------------------------------------------------------
# # get device or service  appointments and info
################ API FOR GET DEVICE INFO ##############################
#-----------------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def device_info(request):
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
          device_name = body['deviceName']
          device = Device.objects.get(name=device_name)
          #spez = device.specialization if device.specialization is not None else '-'
          description = device.description if device.description is not None else '-'
          img = device.photo.url
          result = 'ok'
          return JsonResponse({
               'result':result,
               'name':device_name,
               #'specialization':spez,
               'descriptipn':desc_lines(description),
               'image' : img,
               
          })
     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : "invalid data",
          })
#----------------------------------------------------------
########### API FOR GET DEVICE SCHEDULE  ##################
#---------------------------------------------------------- 
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def therapist_schedule(request):
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
          device_name = body['deviceName']
          therapist_name = body['therapistName']
          device = Device.objects.get(name=device_name)
          if therapist_name == '-':
               therapist_name = Therapist.objects.get()
          available_appointmnets_list = get_competent_schedule_in_month(therapist_name,False)
          if  not device.is_service:
               for day_presence in available_appointmnets_list:
                    device_reserved_appointmnets = get_device_reserved_appointments_in_day(device,day_presence['day'])
                    for appointment in device_reserved_appointmnets:
                         for appo in day_presence['timeList']:
                              if str(appointment['time'])[0:-3] == appo['time']:   
                                   appo['free'] = False
                                   break                     

          result = 'ok'
          return JsonResponse({
               'result':result,
               'schedule':available_appointmnets_list,
            
          })
     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : "invalid data",
          })
#----------------------------------------------------------
########### API FOR GET THERAPIST INFO   ##################
#---------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def therapist_info(request):
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
          therapist_name = body['therapistName']
          therapist = Therapist.objects.get(name=therapist_name)
          spez = therapist.specialization if therapist.specialization is not None else '-'
          description = therapist.description if therapist.description is not None else '-'
          img = therapist.photo.url
          result = 'ok'
          return JsonResponse({
               'result':result,
               'name':therapist_name,
               'specialization':spez,
               'descriptipn':desc_lines(description),
               'image' : img,
          })
     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : 'invalid data',
          })
#----------------------------------------------------------
########### API FOR GET Device Therapist   ################
#---------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def device_therapists(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'PATIENT':
               return JsonResponse({
                      'result':result,
                      'message':'you don\'t have permission to do this action'
              })
          therapists_list =[]
          all_therapists = Therapist.objects.all()
          for therapist in all_therapists:
               therapist_details = {
                    'name':therapist.name,
                    'image':therapist.photo.url,
                    'specialization':therapist.specialization,
                    'description':desc_lines(therapist.description)[0],
                    'is_doctor':False,
               }
               therapists_list.append(therapist_details)

          result = 'ok'
          return JsonResponse({
               'result':result,
               'therapistList':therapists_list
          })
     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : 'invalid data',
          })
#----------------------------------------------------------
########### API FOR RESERVE Device APPOINTMENT ############
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def reserve_device_appointment(request):
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
          therapist_name = body['therapistName']
          device_name = body['deviceName']
          appointment_date = body['appointmentDate']
          appointment_time = body['appointmentTime'] +":00"
          patient = user
          therapist = Therapist.objects.get(name=therapist_name)
          print('1')
          device = Device.objects.get(name=device_name)
          print('1')
          device_appointments_checks = device_appointment.objects.filter(date=appointment_date,time=appointment_time,device=device).exists() if device.is_service == False else False
          therapist_appointments_checks = device_appointment.objects.filter(date=appointment_date,time=appointment_time,therapist=therapist).exists()
          patient_appointments_checks = doctor_appointment.objects.filter(date=appointment_date,time=appointment_time,patient=patient).exists() or  device_appointment.objects.filter(date=appointment_date,time=appointment_time,patient=patient).exists()
          if not device_appointments_checks:
               if not therapist_appointments_checks:
                    if not patient_appointments_checks:
                         therapist_available_appointments = get_available_competent_appointments_in_month(therapist_name,False)
                         for appoint in therapist_available_appointments:
                              if appointment_date == appoint['date'] :
                                   if appointment_time in appoint['availableAppointments']:
                                        appointment = device_appointment()
                                        appointment.device = device
                                        appointment.therapist = therapist
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
                                        'message':'therapist is not available in this time',
                                        })
                         return JsonResponse({
                                        'result':result,
                                        'message':'therapist is not available in this day',
                                        })           
                                   
                    else:
                         return JsonResponse({
                         'result':result,
                         'result':'You   have an appointment in '+str(appointment_date)+' at  '+str(appointment_time)+' oclock already '
                         })
               else:
                    return JsonResponse({
                         'result':result,
                         'messagee':'Therapist  have an appointment in '+str(appointment_date)+' at  '+str(appointment_time)+' oclock already ',
                    })
          else:
               return JsonResponse({
                  'result':result,
                  'messagee':'device  have an appointment in '+str(appointment_date)+' at  '+str(appointment_time)+' oclock already ',  
               })
     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : 'invalid data',
               'err':str(e)
          })
#----------------------------------------------------------
############# API FOR GET MY APPOINTMENTS #################
#----------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def my_appointments(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'PATIENT':
               return JsonResponse({
                      'result':result,
                      'message':'you don\'t have permission to do this action'
              })
          previous_aapointment = []
          upcoming_appointment = []
          my_device_appointments = device_appointment.objects.filter(patient=user)
          my_doctor_appointments = doctor_appointment.objects.filter(patient=user)
          for appointment in my_doctor_appointments:
               details = {
                    'date':appointment.date,
                    'time' : appointment.time.strftime('%H:%M'),
                    'sectionName':appointment.doctor.section.name,
                    'competentName':appointment.doctor.name,
                    'deviceName':None,
               }
               if switch(appointment) == 'pre':
                    previous_aapointment.append(details)
               else : 
                    upcoming_appointment.append(details)     
                    
          for appointment in my_device_appointments:
               details = {
                    'date':appointment.date,
                    'time' :appointment.time.strftime('%H:%M'),
                    'sectionName':appointment.device.section.name,
                    'competentName':appointment.therapist.name,
                    'deviceName':appointment.device.name,
               }
               
               if switch(appointment) == 'pre':
                    previous_aapointment.append(details)
               else : 
                    upcoming_appointment.append(details)     
                         

          # previous_aapointment.reverse()
          # upcoming_appointment.reverse()
          result = 'ok'
          return JsonResponse({
               'result':result,
               'previous':previous_aapointment,
               'upcoming':upcoming_appointment,
          })
     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : 'invalid data',
          })
#----------------------------------------------------------
############### API FOR NOTIFICATIONS   ###################
#----------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def notifications(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'PATIENT':
               return JsonResponse({
                      'result':result,
                      'message':'you don\'t have permission to do this action'
              })
          my_appointments_notificaton = []
          my_device_appointments = device_appointment.objects.filter(patient=user)
          my_doctor_appointments = doctor_appointment.objects.filter(patient=user)
          for appointment in my_doctor_appointments:
               details = {
                    'date':appointment.date,
                    'time' : appointment.time.strftime('%H:%M'),
                    'sectionName':appointment.doctor.section.name,
                    'competentName':appointment.doctor.name,
                    'deviceName':None,
                    'id' : appointment.id,
                    'doctorAppointment': True,

                   
               }
               my_appointments_notificaton.append(details)
               if switch(appointment) == 'upcom':
                    details['type'] = 'waiting'
               elif switch(appointment) == 'pre':
                    if not appointment.attended:
                        details['type'] = 'Missed'
                    elif  not rate.objects.filter(doctor_appointment=appointment).exists(): 
                         details['type'] = 'Rate'      
                    else:
                         my_appointments_notificaton.remove(details)
                         
          for appointment in my_device_appointments:
               details = {
                    'date':appointment.date,
                    'time' : appointment.time.strftime('%H:%M'),
                    'sectionName':appointment.device.section.name,
                    'competentName':appointment.therapist.name,
                    'deviceName':appointment.device.name,
                    'id' : appointment.id,
                    'doctorAppointment': False,
                    
               }
               my_appointments_notificaton.append(details)
               if switch(appointment) == 'upcom':
                    details['type'] = 'waiting'
               elif switch(appointment) == 'pre':
                    if not appointment.attended:
                        details['type'] = 'Missed'
                    elif  not rate.objects.filter(device_appointment=appointment).exists(): 
                         details['type'] = 'Rate'      
                    else:
                         my_appointments_notificaton.remove(details)
          result = 'ok'
          return JsonResponse({
               'result':result,
               'notifications':my_appointments_notificaton,
          })               


     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : 'invalid data',
               'err':str(e)
          })
#----------------------------------------------------------
############ API FOR RATING AN APPOINTMENT ################
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def rate_appointment(request):
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
          appointment_id = body['id']
          is_doctor_appointment = body['doctorAppointment']
          cleanless = body['cleanless']
          treatment_od_medical_staff = body['treatment_od_medical_staff']
          therapisting_rate = body['therapisting_rate']
          reception_rate = body['reception_rate']
          if is_doctor_appointment:
               appointment = doctor_appointment.objects.get(id=appointment_id)
               section = appointment.doctor.section
               name_of_competent = appointment.doctor.name
          else:
               appointment = device_appointment.objects.get(id=appointment_id)
               section = appointment.device.section
               name_of_competent = appointment.therapist.name
          my_rate = rate()
          my_rate.patient = user
          my_rate.section = section
          my_rate.name_of_th_therapist = name_of_competent
          my_rate.cleanless = cleanless
          my_rate.therapisting_rate = therapisting_rate
          my_rate.treatment_od_medical_staff = treatment_od_medical_staff
          my_rate.reception_rate = reception_rate
          if is_doctor_appointment:
               my_rate.doctor_appointment = appointment
          else:
               my_rate.device_appointment = appointment     
          my_rate.save()
          result = 'ok'
          return JsonResponse({
               'result': result,
               'message': 'succsses'
          })

     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : 'invalid data',
               'err':str(e)
          })
#----------------------------------------------------------
################ API FOR EDIT PROFILE #####################
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def edit_profile(request):
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
          gender = body['gender']
          relationship = body['relationship']
          img = body['profile_picture']
          phone_number = body['phoneNumber']
          birth_date = body['birth_date']

          profile = PatientProfile.objects.get(user=user)
          if  not gender == '-':
               profile.gender = 'F' if gender == '1' else 'M'
          if not relationship == '-':
               profile.relationship = 'S' if relationship=='1' else 'M'     
          if not phone_number =='-':
               profile.phone_number = phone_number
          if not birth_date == '-':
               profile.birth_date = birth_date
          if not img == '-':
                    format, imgstr = img.split(';base64,') 
                    ext = format.split('/')[-1] 
                    patient_img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                    profile.img = patient_img
          profile.save()
          result = 'ok'
          return JsonResponse({
               'result':result,
               'message':'edited successfully'
          })


     except Exception as e:
          return JsonResponse({
               'result':result,
               'message' : 'invalid data',
               'err':str(e)
          })


