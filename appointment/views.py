from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view,permission_classes
from datetime import datetime,date,timedelta,time
from .models import doctor_appointment,device_appointment,Doctor,Device,Therapist
from account.models import Patient,User
from account.models import PatientProfile
import json
import calendar
from rest_framework.permissions import IsAuthenticated

################ API FOR REACT APP  for employee ######################
#----------------------------------------------------------------------
##############Function For Help ########################################
def sort_by_date_joined(list):
     return list['date_joined']
#-----------------------------------------------------------------------
def sorting(lis):
     return lis['time']
#----------------------------------------------------------------------
def date_sorting(list):
     return list['date']
#----------------------------------------------------------------------
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
#---------------------------------------------------------------------- 
def calculateAge(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) <
         (birthDate.month, birthDate.day))
 
    return age
#----------------------------------------------------------------------
def get_competent_schedule_in_day(name,is_doctor):
      appointmet_period = 30
      if is_doctor: 
           doctor = Doctor.objects.get(name=name)
      else:
           doctor = Therapist.objects.get(name=name)    
      date_format = "%H:%M:%S"
      start_hours_in = str(doctor.start_hours_in)
      end_hours_in = str(doctor.end_hours_in)
      diff = datetime.strptime(end_hours_in, date_format) - datetime.strptime(start_hours_in, date_format)
      time_in_minutes = int(diff.seconds / 60) 
      appointment_list_in_day=[]
      start_hours_in =  datetime.strptime(start_hours_in, date_format)
      for appointment_shift_time in range(0,time_in_minutes,appointmet_period):         
          appointment_time = datetime.strftime(start_hours_in + timedelta(minutes=appointment_shift_time),date_format)
                   
                       
          appointment_list_in_day.append(appointment_time)
      return appointment_list_in_day
#----------------------------------------------------------------------
def get_competent_days_in_week(name,is_doctor):
     if is_doctor:
          competent = Doctor.objects.get(name=name)
     else:
          competent = Therapist.objects.get(name=name)
     if competent is None:
          return 'there is no comptent with this name'
     else:
           daysIn = []
           daysIn.append('Saturday') if competent.saturday==True else None
           daysIn.append('Sunday') if competent.sunday==True else None
           daysIn.append('Monday') if competent.monday==True else None 
           daysIn.append('Tuesday') if competent.tuesday==True else None
           daysIn.append('Wednesday') if competent.wednesday==True else None
           daysIn.append('Thursday') if competent.thursday==True else None
           daysIn.append('Friday') if competent.friday==True else  None
           return daysIn
#----------------------------------------------------------------------
def get_available_competent_appointments_in_month(name,is_doctor):
     competent_days_in_week = get_competent_days_in_week(name,is_doctor)   
     start_date = date.today()
     end_date = start_date  + timedelta(days=30)
     # print(competent_days_in_week)
     # print(start_date)
     # print(end_date)
     monthly_presence =[]
     for day in daterange(start_date, end_date):     
          if calendar.day_name[day.weekday()] in competent_days_in_week:
               available_appointments = get_available_competent_appointments_in_day(name,is_doctor,day)
               day_presence = {
                    'weekDay':calendar.day_name[day.weekday()],
                    'date': day.strftime("%Y-%m-%d"),
                    'availableAppointments':available_appointments,
                     
               }
               monthly_presence.append(day_presence)

     return monthly_presence
#----------------------------------------------------------------------
def get_available_competent_appointments_in_day(name,is_doctor,date):
     appointment_list = get_competent_schedule_in_day(name,is_doctor)
     if is_doctor:
          doctor = Doctor.objects.get(name=name)
          reserved_appointment = doctor_appointment.objects.filter(doctor= doctor,date= date)     
     else:
          therapist = Therapist.objects.get(name=name)
          reserved_appointment = device_appointment.objects.filter(therapist=therapist,date=date)
     for appointment in reserved_appointment:
              
               if str(appointment.time) in appointment_list:
                    appointment_list.remove (str(appointment.time))
     return appointment_list
#----------------------------------------------------------------------
def get_reserved_appointments_in_day(name,is_doctor,date):
     appointment_list =[]
     if is_doctor:
          doctor = Doctor.objects.get(name=name)
          reserved_appointment = doctor_appointment.objects.filter(doctor= doctor,date= date)     
     else:
          therapist = Therapist.objects.get(name=name)
          reserved_appointment = device_appointment.objects.filter(therapist=therapist,date=date) 
     for appointment in reserved_appointment:
          profile = PatientProfile.objects.get(user = appointment.patient)
          appointment_details = {
               'patientName':appointment.patient.username if appointment.patient.username else '-',
               'time':appointment.time if appointment.time  else '-',
               'fileNumber': profile.file_number if profile.file_number else '-',
               'attend':appointment.attended if appointment.attended is not None else '-',
               'appointment_id':appointment.id,
               'is_doctor':is_doctor,

          }
          appointment_list.append(appointment_details)
     return appointment_list
#------------------------------------------------------------------------
def get_reserved_competent_appointments(name,is_doctor):      
     competent_days_in_week = get_competent_days_in_week(name,is_doctor)   
     start_date = date.today()
     end_date = start_date  + timedelta(days=30)
     monthly_reserved_appointment =[]
     for day in daterange(start_date, end_date):     
          if calendar.day_name[day.weekday()] in competent_days_in_week:
               reserved_appointments = get_reserved_appointments_in_day(name,is_doctor,day)
               if reserved_appointments.__len__() > 0:

                    day_reserves = {
                         'weekDay':calendar.day_name[day.weekday()],
                         'date': day.strftime("%Y-%m-%d"),
                         'reservedAppointments':reserved_appointments,
                         
                    }
                    monthly_reserved_appointment.append(day_reserves)
     return monthly_reserved_appointment
#----------------------------------------------------------------------
def get_device_reserved_appointments_in_day(device,date):
     appointments_list =[]
     #device = Device.objects.get(name=name,date=date)
     reversed_appointments = device_appointment.objects.filter(device=device,date=date)
     for appointment in reversed_appointments:
          profile = PatientProfile.objects.get(user = appointment.patient)
          appointment_details = {
               'patientName':appointment.patient.username if appointment.patient.username else '-',
               'time':appointment.time if appointment.time  else '-',
               'fileNumber': profile.file_number if profile.file_number else '-',
               'attend':appointment.attended if appointment.attended is not None else '-',
               'competentName':appointment.therapist.name if appointment.therapist.name else'-',
               'appointment_id':appointment.id,
               'is_doctor':False,

          }
          appointments_list.append(appointment_details)
     return appointments_list
#----------------------------------------------------------------------
def get_device_reserved_appointments(name):
     device = Device.objects.get(name=name)
     start_date = date.today()
     end_date = start_date  + timedelta(days=30)
     monthly_reserved_appointment =[]
     for day in daterange(start_date, end_date):
          if device.active:
               reserved_appointments = get_device_reserved_appointments_in_day(device,day)
               if reserved_appointments.__len__() > 0:
                    day_reserves = {
                         'weekDay':calendar.day_name[day.weekday()],
                         'date': day.strftime("%Y-%m-%d"),
                         'reservedAppointments':reserved_appointments,
                         
                    }
                    monthly_reserved_appointment.append(day_reserves)
     return monthly_reserved_appointment
#----------------------------------------------------------------------
################ GET TODAY'S APPOINTMENTS #############################

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def today_appointments(request):
    try:
        

        result = 'invalid'
        user = request.user
        if user.role != 'RECEIPTION':
          return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })    
        today = date.today()
        today_doctors_appointments = doctor_appointment.objects.filter(date=today)
        today_devices_appointments = device_appointment.objects.filter(date=today)

        today_appointments = []
        for appointment in today_doctors_appointments:
               profile = PatientProfile.objects.get(user = appointment.patient)
               
               
               x = {
               'Name':appointment.patient.username if appointment.patient.username is not None else '-',
               'FileNumber':profile.file_number if profile.file_number is not None else '-',
               'Section':appointment.doctor.section.name if appointment.doctor.section.name is not None else '-',
               'Competent':appointment.doctor.name if appointment.doctor.name is not None else '-',
               'attend':appointment.attended if appointment.attended is not None else '-',
               'time': appointment.time if appointment.time is not None else '-',
               'appointment_id':appointment.id,
               'is_doctor':True,
                    }
               today_appointments.append(x)
        for appointment in today_devices_appointments:
                    profile = PatientProfile.objects.get(user = appointment.patient)
                    x = {
                    'Name':appointment.patient.username if appointment.patient.username is not None else '-',
                         'FileNumber':profile.file_number if profile.file_number is not None else '-',
                         'Section':appointment.therapist.section.name if appointment.therapist.section.name is not None else '-',
                         'Competent':appointment.therapist.name if appointment.therapist.name is not None else '-',
                         'attend':appointment.attended if appointment.attended is not None else '-',   
                         'time': appointment.time if appointment.time is not None else '-',
                         'appointment_id':appointment.id,
                         'is_doctor':False,

                         
                         }
                    today_appointments.append(x)
        result = 'ok'  
        if today_appointments.__len__() ==0:  
               return JsonResponse({
                    'result':result,
                    'message':'there is no appointments today'
                                   })
        else:
               today_appointments.sort(key=sorting)
               return JsonResponse({
                    'result':result,
                    'appointment':today_appointments,
                                   })
    except:
        return JsonResponse({
                'result':result,
                'message':'invalid request'
                                })    
#----------------------------------------------------------------
################ API FOR GET DOCTORS LIST ######################
#---------------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def Doctors(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
           return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })          
          all_doctors = Doctor.objects.all()
          doctor_list = []
          for doctor in all_doctors:
               daysIn = []
               daysIn.append('saturday') if doctor.saturday==True else None
               daysIn.append('sunday') if doctor.sunday==True else None
               daysIn.append('monday') if doctor.monday==True else None
               daysIn.append('tuesday') if doctor.tuesday==True else None
               daysIn.append('wednesday') if doctor.wednesday==True else None
               daysIn.append('thursday') if doctor.thursday==True else None
               daysIn.append('friday') if doctor.friday==True else  None
               daysin = ' - '.join([str(elem) for i,elem in enumerate(daysIn)])

               
               
               doctor_details = {
                    'Name':doctor.name if doctor.name is not None else '-',
                    'Section':doctor.section.name if doctor.section.name is not None else '-',
                    'Presence':daysin,
                    }
               doctor_list.append(doctor_details)
          result = 'ok'         
          return JsonResponse({
                    'result':result,
                    'Doctors':doctor_list,
               })      
     except:
         return JsonResponse({
                    'result':result,
               }) 
#---------------------------------------------------------------
################ HANDLE WITH NOT ATTENDED APPOINTMENT   ########
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def not_attend_appointment(request):
     try:
         result = 'invalid'
         user = request.user
         if user.role != 'RECEIPTION':
           return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         
         body_unicode = request.body.decode('utf-8')
         body = json.loads(body_unicode)
         appointment_id = body['appointment_id']
         is_doctor = body['is_doctor']
         if is_doctor :
            appointment = doctor_appointment.objects.get(id = appointment_id)
     
         else:
              appointment = device_appointment.objects.get(id = appointment_id)
         if appointment.attended :
              appointment.attended = False
              appointment.save()
              #send notififcation to mobile app
              result = 'ok'
              return JsonResponse({
                   'result':result,
                   'message':"sucsess"
              })       
         else:
               return JsonResponse({
               'result':result,
               'messag':'the appointment is not attended   already'
          })
              
     except:
          return JsonResponse({
               'result':result,
               'messag':'the appointment is not exists'
          })
#---------------------------------------------------------------
################ HANDLE WITH NOT ATTENDED APPOINTMENT   ########
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def attend_appointment(request):
     try:
         result = 'invalid'
         user = request.user
         if user.role != 'RECEIPTION':
           return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         
         body_unicode = request.body.decode('utf-8')
         body = json.loads(body_unicode)
         appointment_id = body['appointment_id']
         is_doctor = body['is_doctor']
         if is_doctor :
            appointment = doctor_appointment.objects.get(id = appointment_id)
     
         else:
              appointment = device_appointment.objects.get(id = appointment_id)
         if appointment.attended == False :
              appointment.attended = True
              appointment.save()
              #send notififcation to mobile app
              result = 'ok'
              return JsonResponse({
                   'result':result,
                   'message':"sucsess"
              })       
         else:
               return JsonResponse({
               'result':result,
               'messag':'the appointment is  attended  already'
          })
              
     except:
          return JsonResponse({
               'result':result,
               'messag':'the appointment is not exists'
          })     
#---------------------------------------------------------------
################ API FOR GET DOCTOR SCHEDULE  IN MONTH #########
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def see_schedule(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          doctor_name = body['name']
          available_competent_appointments_in_month = get_available_competent_appointments_in_month(doctor_name,True)
          reserved_competent_appointments = get_reserved_competent_appointments(doctor_name,True)
          result = 'ok'   
             
               
          return JsonResponse({
               'result':result,
               'name':doctor_name,
               'monthlyPresence': available_competent_appointments_in_month,
               'ReservedAppointments': reserved_competent_appointments,            
                            })        
     except:
          return JsonResponse({
               'result':result,
               'message':'doctor '+ doctor_name+' is not exists'
          })
#----------------------------------------------------------------
############## API FOR DELETE  APPOINTMENT ################
#----------------------------------------------------------------
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_appointment(request):
         try:
             result = 'invalid'
             user = request.user
             if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

             body_unicode = request.body.decode('utf-8')
             body = json.loads(body_unicode)
             is_doctor = body['is_doctor']
             id = body['appointment_id']
             if is_doctor:
                  appointment = doctor_appointment.objects.get(id=id)
             else:
                  appointment = device_appointment.objects.get(id=id)
             appointment.delete()
             result ='ok'
             return JsonResponse({
                  'result':result,
                  'message':'appointment deleted'
             })          
         except:
               return JsonResponse({
                  'result':result,
                  'message':'success'
             }) 
#----------------------------------------------------------------
############## API FOR edit  APPOINTMENT ################
#----------------------------------------------------------------    
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def edit_appointment(request):
         try:
             result = 'invalid'
             user = request.user
             if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

             body_unicode = request.body.decode('utf-8')
             body = json.loads(body_unicode)
             is_doctor = body['is_doctor']
             id = body['appointment_id']
             new_date = body['date']
             new_time = body['time']

             if is_doctor:
                  
                  appointment = doctor_appointment.objects.get(id=id)
                  name = appointment.doctor.name
                  appointments = doctor_appointment.objects.filter(date=new_date,time=new_time).exists()
                  th_appointmemts = False
                  
             else:
                 
                  appointment = device_appointment.objects.get(id=id)
                  th = appointment.therapist
                  name = appointment.therapist.name
                  appointments = device_appointment.objects.filter(date=new_date,time=new_time).exists()
                  th_appointmemts = device_appointment.objects.filter(date=new_date,time=new_time,therapist=th).exists() 

             if not appointments and not th_appointmemts:
                  available_appointments = get_available_competent_appointments_in_month(name,is_doctor)
                  for appoint in available_appointments:
                       if new_date == appoint['date'] :
                            if new_time in appoint['availableAppointments']:
                              appointment.date = new_date
                              appointment.time = new_time
                              appointment.save()
                              result ='ok'
                              return JsonResponse({
                                      'result':result,
                                      'message':'edit successfuly'
                                 })
                            else:
                                   return JsonResponse({
                                         'result':result,
                                         'message':'competent '+name+' did not come on this date '+str(new_date)+' or this time '+str(new_time),
                                          })               
             else:
                                 
               return JsonResponse({
                         'result':result,
                         'messagee':'Competent '+name+' have an appointment in '+str(new_date)+' at  '+str(new_time)+' oclock already ',
                                          })
                  
         except:
               return JsonResponse({
                  'result':result,
                  'message':'invalid data'
             })    
#----------------------------------------------------------------
######### API FOR GET DEVICES LIST ##############################
#----------------------------------------------------------------     
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def Devices(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role not in ['RECEIPTION','APPMANAGER']:
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          all_devices = Device.objects.all()
          device_list = []
          for device in all_devices:
               device_details ={
                    'Name':device.name if device.name else '-',
                    'Section':device.section.name if device.section.name else '-',
                    'active':'Yes' if device.active else 'No',

               }
               device_list.append(device_details)
          result = 'ok'     
          return JsonResponse({
               'result':result,
               'Devices':device_list,

          })     

     except:
          return JsonResponse({
               'result':result,
               'message':'bad request'
          })
#----------------------------------------------------------------
######### API FOR GET PATIENTS LIST ##############################
#---------------------------------------------------------------- 
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def Patients(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          all_patients = Patient.patient.all()
          patients_list = []
          for patient in all_patients:
               patient_profile = PatientProfile.objects.get(user = patient) 
               patient_details = {
                     'Name':patient.username if patient.username else '-',
                     'FileNumber':patient_profile.file_number if patient_profile.file_number else '-',
                     'Gender':'Male' if patient_profile.gender=='M' else 'Female',
                     'Age': calculateAge(patient_profile.birth_date) if patient_profile.birth_date else '-',
                     'date_joined':patient.date_joined 

               }
               patients_list.append(patient_details)
          patients_list.sort(key=sort_by_date_joined,reverse=True)
               
          result ='ok'
          return JsonResponse({
               'result1':result,
               'Patients':patients_list,
                               })
     except Exception as e:
          return JsonResponse({
               'result':result,
               'message':str(e)
          })
#----------------------------------------------------------------
######### API FOR add DOCTOR LIST ##############################
#---------------------------------------------------------------- 
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_doctor_appointment(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          patient_name = body['patientName']
          doctor_name = body['doctorName']
          appointment_date = body['appointmentDate']
          appointment_time = body['appointmentsTime']
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
#---------------------------------------------------------------
############# API FOR ADD PATIENT ##############################
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_patient(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          patient_name = body['patientName']
          password = body['password']
          birth_date = body['birthDate']
          gender = body['gender']
          relationship = body['relationship']
          phone_number = body['phoneNumber']
          file_number = body['fileNumber']
          if Patient.patient.filter(username=patient_name).exists() or PatientProfile.objects.filter(file_number=file_number).exists():
               return JsonResponse({
                    "result":result,
                    'message':'you already have an account',
               })
          else:
                regex = datetime.strptime
                if  regex(birth_date,'%Y-%m-%d'):
                    
                    patient = Patient.objects.create_user(
                    username = patient_name,
                    password  = password,  
                                             ) 
                    patient.save()
                    profile = PatientProfile.objects.get(user=patient) 
                    profile.phone_number = phone_number
                    profile.birth_date = birth_date
                    profile.gender = 'F' if gender == 1 else  'M'
                    profile.relationship = 'S' if relationship == 1 else 'M'
                    profile.file_number = file_number
                    profile.save()
                    result = 'ok'
                    return JsonResponse({
                         'result':result,
                         'message':'patient added successfuly',
                    })
                
                
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid data',
          })
#---------------------------------------------------------------
############# API FOR GET PATIENT APPOINTMENTS #################
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def patient_appointments(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          patient_name = body['Name']

          patient = Patient.patient.get(username=patient_name)
         
          profile = PatientProfile.objects.get(user =patient)
        
          doctors_appointments = doctor_appointment.objects.filter(patient=patient)
       
          devices_appointments = device_appointment.objects.filter(patient = patient)
         
          file_number = profile.file_number if profile.file_number is not None else '-'
          today = date.today()
          now = datetime.now()
          current_time = now.strftime("%H:%M:%S")
          patient_appointments = []
          for appointment in doctors_appointments:
               status = 'Waiting'
               
               if appointment.date - today == timedelta(0):
                    print(type(datetime.combine(date.today(),appointment.time)))
                    print(type(now))          
                    if now > datetime.combine(date.today(),appointment.time) :
                              if appointment.attended :
                                   status = 'Attended'
                              else:
                                   status = 'Missed'
                    else:
                         status = 'Waiting'                                 
               elif today > appointment.date:
                    
                            if appointment.attended :
                                  status = 'Attended'
                            else:
                                  status = 'Missed'     

               x = {
             'date':appointment.date if appointment.date else '-',
             'time': appointment.time if appointment.time is not None else '-',
             'Section':appointment.doctor.section.name if appointment.doctor.section.name is not None else '-',
             'Competent':appointment.doctor.name if appointment.doctor.name is not None else '-',
             'status':status, 
             'appointment_id':appointment.id,
             'is_doctor':True,
                }
               patient_appointments.append(x)
          for appointment in devices_appointments:
               status = 'Waiting'
               
               if appointment.date - today == timedelta(0):
                    print(type(datetime.combine(date.today(),appointment.time)))
                    print(type(now))          
                    if now > datetime.combine(date.today(),appointment.time) :
                              if appointment.attended :
                                   status = 'Attended'
                              else:
                                   status = 'Missed'
                    else:
                         status = 'Waiting'                                 
               elif today > appointment.date:
                    
                            if appointment.attended :
                                  status = 'Attended'
                            else:
                                  status = 'Missed'     
               x = {
                     'date':appointment.date if appointment.date else '-',
                     'time': appointment.time if appointment.time is not None else '-',
                     'Section':appointment.therapist.section.name if appointment.therapist.section.name is not None else '-',
                     'Competent':appointment.therapist.name if appointment.therapist.name is not None else '-',
                     'status':status,
                     'appointment_id':appointment.id,
                     'is_doctor':False,

                    
                     }
               patient_appointments.append(x)
          result = 'ok'
          if patient_appointments.__len__() == 0:
               return JsonResponse({
                    'result':result,
                    'fileNumber':file_number,
                    'Name':patient_name,
                    'message':' then patient  don\'t have any appointmants',
               }) 
          else:
               patient_appointments.sort(key=date_sorting)
               return JsonResponse({
                    'result':result,
                    'fileNumber':file_number,
                    'Name':patient_name,
                    'appointments': patient_appointments

               })
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid data'
          })
#---------------------------------------------------------------
############# API FOR GET THERAPISTS NAMES #####################
#---------------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def therapists_names(request):
     try:
          result = "invalid"
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          all_therapists = Therapist.objects.all()
          therapists_list =[]
          for therapist in all_therapists:
               therapist_name = therapist.name
               therapists_list.append(therapist_name)
          result = 'ok' 
          return JsonResponse({
               'result':result,
               'names':therapists_list,
          })
     except:
          return JsonResponse({
               'result':result,
               'message':'invaild data'
          })    
#---------------------------------------------------------------
############# API FOR GET DEVICE WITH TECHNICAL APPOINTMENTS ###
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def available_dt_appointments(request):
     try: 
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          device_name = body['deviceName']
          therapist_name = body['therapistName']
          device = Device.objects.get(name=device_name)
          available_appointmnets_list = get_available_competent_appointments_in_month(therapist_name,False)
          # available_appointments= []
          if  not device.is_service:
               for day_presence in available_appointmnets_list:
                    # print(day_presence)
                    device_reserved_appointmnets = get_device_reserved_appointments_in_day(device,day_presence['date'])
                    for appointment in device_reserved_appointmnets:
                         if str(appointment['time']) in day_presence['availableAppointments']:
                              day_presence['availableAppointments'].remove(str(appointment['time']))                    
          result ='ok'               
          return JsonResponse({
               'result':result,
               'availableAppointments':available_appointmnets_list
          })

     



          
     except:
          return JsonResponse({
               'result':result,
               'messsage':'invalid data'
          })
#---------------------------------------------------------------
############# API FOR GET DEVICE RESERVED ######################
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def device_reserved_appointments(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          device_name = body['name']
          print(device_name)
          device_reserved_appointments = get_device_reserved_appointments(device_name)
          result = 'ok'   
                  
          return JsonResponse({
               'result':result,
               'name':device_name,
               'ReservedAppointments': device_reserved_appointments,            
                            })        
     except:
          return JsonResponse({
               'result':result,
               'message':'device '+ device_name +' is not exists'
          })          
#---------------------------------------------------------------
############# API FOR RESERVE DEVICE APPOINTMENT################
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_device_appointment(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         

          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          patient_name = body['patientName']
          therapist_name = body['therapistName']
          device_name = body['deviceName']
          appointment_date = body['appointmentDate']
          appointment_time = body['appointmentsTime']
          patient = Patient.objects.get(username=patient_name)
          
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
     except:
          return JsonResponse(({
               'result':result,
               'message':"invalid data"}))
#---------------------------------------------------------------
################ PATIENT INFO ##################################
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def patient_info(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })         
          body_unicode = request.body.decode('utf-8')
          body = json.loads(body_unicode)
          patient_name = body['Name']
          patient = Patient.patient.get(username=patient_name)
          profile = PatientProfile.objects.get(user =patient)
          file_number = profile.file_number  if profile.file_number is not None else '-'
          phone_number = profile.phone_number  if profile.phone_number is not None else '-'
          bdate = profile.birth_date  if profile.birth_date is not None else '-'
          gender = '1' if  profile.gender=='F' else '0'
          rel = '1' if profile.relationship == 'S' else '0'
          result = 'ok'
          return JsonResponse({
               'result':result,
               'patientName' : patient_name,
               'gnender': gender,
               'relationship':rel,
               'birthDate':bdate,
               'phoneNumber':phone_number,
               'file_number':file_number
          })
     except :
          return JsonResponse(({
               'result':result,
               'message':'invalid data'}))
    
#---------------------------------------------------------------
################ API FOR EDIT PATIENTS #########################
#---------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def edit_patient(request):
     try:
          result = 'invalid'
          user = request.user
          if user.role != 'RECEIPTION':
               return JsonResponse({
                'result':result,
                'message':'you don\'t have permission to this action'
                                })
          name = request.POST['patientName']
          file_number = request.POST.get("fileNumber",None)
          phone_number = request.POST.get("phoneNumber",None)
          bdate = request.POST.get("birthDate",None)
          gender = request.POST.get("gender",None)
          relationship = request.POST.get("relationship",None)
          password = request.POST.get("password",None)
          patient = Patient.patient.get(username=name)
          profile = PatientProfile.objects.get(user =patient)
          if password is not None :
               user = Patient.objects.get(username=name)
               print(user)
               print(user.password)
               user.set_password(password)
               user.save()
               print(user.password)

               # user = User.objects.get(username=name)
               # print(patient.password)
               # print(user)
               # user.set_password(str(password))
               # print(patient.password)
               # user.save()

               
          if file_number is not None :
               # print(type(file_number))
               # print(type(profile.file_number))
               if  not PatientProfile.objects.filter(file_number=file_number).exists() or str(profile.file_number) == file_number : 
                    profile.file_number  = file_number
               else:
                    return JsonResponse({
                         'result':result,
                         'message':'This file number has been given to another user'
                    })     
          if phone_number is not None : 
               profile.phone_number  = phone_number
          if bdate is not None : 
               profile.birth_date  = bdate
          if gender is not None : 
               profile.gender  = 'F' if  gender == '1' else 'M'
          if relationship is not None : 
               profile.relationship  = 'S' if relationship == '1' else 'M'
          profile.save()
          patient.save()
          result = 'ok'
          return JsonResponse({
               'result': result,
               'message': 'Patient edited successfully'
          })

     except Exception as e:
          return JsonResponse(({
               'result':result,
               'message':str(e)}))
#-----------------------------------------------------------------
################### #########################
#-----------------------------------------------------------------      
     