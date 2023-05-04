from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view,permission_classes
from datetime import datetime,date,timedelta,time
from appointment.models import Post,Instruction,Offer,Doctor,Device,Therapist,Section
from account.models import Patient
from account.models import PatientProfile
import json
import calendar
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from patient.views import desc_lines
#-----------------------------------------------------
def sorting(lis):
    return lis['Name']
#-----------------------------------------------------
def get_doctors_list():
    doctors_list = []
    all_doctors = Doctor.objects.all()
    for doc in all_doctors:
        doctor_details  = {
            'Name':doc.name,
            'Section':doc.section.name,
            'Specialization' : doc.specialization,
        }
        doctors_list.append(doctor_details)
    doctors_list.sort(key=sorting) 
    return doctors_list
#-------------------------------------------------
def get_therapists_list():
    therapists_list = []
    all_therapists = Therapist.objects.all()
    for ther in all_therapists:
        therapist_details  = {
            'Name':ther.name,
            'Section':ther.section.name,
            'Specialization' : ther.specialization,
        }
        therapists_list.append(therapist_details)
    therapists_list.sort(key=sorting) 
    return therapists_list   
########## ADD  TO THE CENTER ##################
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_post(request):
     result = 'invalid'
     try:
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        # body_unicode = request.body.decode('utf-8')
        # body = json.loads(body_unicode)
        name = request.data["name"]
        image = request.data["postImage"]
        description = request.data["description"]
        print(name)
        if not Post.objects.filter(name=name).exists():
             post = Post()
             post.name = name
             post.photo = image
             post.description = description
             now = timezone.now()
             now = now + timedelta(hours = 3)
             print(now)
             post.publish_date = now
             print(now)
             post.save()
             result = 'ok'
             return JsonResponse({
             'result':result,
              'message':'added successfuly' })
        else:
             return JsonResponse({
                  'result':result,
                  "message" : "post already added",
             })     
      
        
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid data'
          })
#----------------------------------------------------------
########### API FOR ADD MEDICAL INSTRUCTION ###############
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_ins(request):
     result = 'invalid'
     try:
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        # body_unicode = request.body.decode('utf-8')
        # body = json.loads(body_unicode)
        name = request.data["name"]
        image = request.data["insImage"]
        description = request.data["description"]
        print(name)
        if not Instruction.objects.filter(name=name).exists():
             ins = Instruction()
             ins.name = name
             ins.photo = image
             ins.description = description
             ins.save()
             result = 'ok'
             return JsonResponse({
             'result':result,
              'message':'added successfuly' })
        else:
             return JsonResponse({
                  'result':result,
                  "message" : "post already added",
             })     
      
        
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid data'
          })
#----------------------------------------------------------
################ API FOR ADD THERAPIST #####################
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_therapist(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["name"]
        image = request.data["therapistImage"]
        specialization = request.data["specialization"]
        description = request.data["description"]
        section_name = request.data["sectionName"]
        print('1')
        saturday = request.data["saturday"] 
        sunday = request.data["sunday"]  
        monday =  request.data["monday"]  
        tuesday = request.data["tuesday"]  
        wednesday =  request.data["wednesday"]  
        thursday = request.data["thursday"]  
        friday =  request.data["friday"] 
        print('2')
        start_hours_in = request.data["startHoursIn"]  
        end_hours_in = request.data["endHoursIn"]
        if not Therapist.objects.filter(name=name).exists():
             section = Section.objects.get(name=section_name)
             therapist  = Therapist()
             therapist.name = name
             therapist.specialization = specialization
             therapist.description = description
             therapist.photo = image
             therapist.section = section
             # the days when therapist comes
             therapist.saturday =True if saturday=='1' else False
             therapist.sunday = True if sunday=='1' else False
             therapist.monday = True if monday=='1' else False
             therapist.tuesday = True if tuesday=='1' else False
             therapist.wednesday = True if wednesday=='1' else False
             therapist.thursday = True if thursday=='1' else False
             therapist.friday = True if friday=='1' else False
             #end days
             therapist.start_hours_in = start_hours_in
             therapist.end_hours_in = end_hours_in
             therapist.save()
             result = 'ok'
             return JsonResponse({
                  'result':result,
                  'message':'added successfuly'
             })
        else:
             return JsonResponse({
                  'result':result,
                  'message':' therapist '+ name +' already exists'
             })  
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })
#----------------------------------------------------------
################# API FOR ADD SECTION #####################
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_section(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["name"]
        image = request.data["sectionImage"]
        if not Section.objects.filter(name=name).exists():  
             section = Section()
             section.name = name
             section.photo = image
             section.save()
             result = 'ok'
             return JsonResponse({
                  'result':result,
                  'message':'added successfuly'
             })
        else:
             return JsonResponse({
                  'result':result,
                  'message':' therapist '+ name +' already exists'
             })  
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })        
#----------------------------------------------------------
################ API FOR ADD DEVICE ######################
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_device(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["name"]
        image = request.data["deviceImage"]
        section_name = request.data["sectionName"]
        description = request.data["description"]
        if not Device.objects.filter(name=name).exists():
             section = Section.objects.get(name=section_name)
             device  = Device()
             device.name = name
             device.photo = image
             device.section = section
             device.description = description
             device.save()
             result = 'ok'
             return JsonResponse({
                  'result':result,
                  'message':'added successfuly'
             })
        else:
             return JsonResponse({
                  'result':result,
                  'message':' device '+ name +' already exists'
             })  
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })
#------------------------------------------------------------
################ API FOR ADD OFFER ##########################
#------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_offer(request):
     result = 'invalid'
     try:
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["name"]
        image = request.data["offerImage"]
        description = request.data["description"]
        start_date = request.data["startDate"]
        end_date = request.data["endDate"]
        old_price  =request.data["oldPrice"]
        new_price = request.data["newPrice"]
        if not Offer.objects.filter(name=name).exists():
             offer = Offer()
             offer.name = name
             offer.photo = image
             offer.description = description
             offer.publish_date = start_date
             offer.ending_date = start_date if end_date == '0' else end_date
             offer.old_price = old_price
             offer.new_price = new_price
             offer.save()
             result = 'ok'
             return JsonResponse({
                'result':result,
              'message':'added successfuly' })
        else:
             return JsonResponse({
                  'result':result,
                  "message" : "post already added",
             })             
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid data'
          })
#------------------------------------------------------------
# GET DEVICES LIST   BASE_URI /appointment/Devices
############# GET DEVICE DATAILS ############################
#------------------------------------------------------------      
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def device_information(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["name"]
        device = Device.objects.get(name=name)
        device_name = device.name
        device_section = device.section.name
        device_picture = device.photo.url
        device_description = desc_lines(device.description)
        is_active = 1 if device.active else 0

        result = 'ok'
        return JsonResponse({
             'result':result,
             'deviceName':device_name,
             'deviceDescription':device_description,
             'deviceImage':device_picture,
             'deviceSection':device_section,
             'isActive': is_active
        })

     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })       
#------------------------------------------------------------
################ API FOR EDIT DEVICE ########################
#------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def edit_device(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["deviceName"]
        image = request.POST.get("deviceImage",0)
        is_active = request.POST.get('isActive',0)
        description = request.POST.get("description",0)
        device = Device.objects.get(name=name)
        if image != 0 :
          device.photo = image
        if description !=0:
          device.description = description
        if is_active !=0:
          device.active = True if is_active == '1' else False
        result = 'ok'
        return JsonResponse({
             'result':result,
             'message':'device edited successfuly'
             
        })

     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })             
#------------------------------------------------------------
################ API FOR DELETE DEVICE ######################
#------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def delete_device(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["name"]
        device = Device.objects.get(name=name)
        device.delete()
        result = 'ok'
        return JsonResponse({
             'result':result,
             'message':'device deleted successfuly'
             
        })
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })
#----------------------------------------------------------     
# DOCTORS AND THERAPIST APIs 
############### GET DOCTORS AND THERAPISTS LIST ###########
#----------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def doctors_therapists(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        all_doctors =get_doctors_list()
        all_therapists = get_therapists_list()
        result = 'ok'
        return JsonResponse({
            'result':result,
            'Doctors':all_doctors,
            'Therapists':all_therapists
        })
     except:
         return JsonResponse({
             'result':result,
             'message':'invalid data'
         })
     
#----------------------------------------------------------
################ API FOR ADD DOCTOR #######################
#----------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_doctor(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["doctorName"]
        image = request.data["doctorImage"]
        specialization = request.data["specialization"]
        description = request.data["description"]
        section_name = request.data["sectionName"]
        print('1')
        saturday = request.data["saturday"] 
        sunday = request.data["sunday"]  
        monday =  request.data["monday"]  
        tuesday = request.data["tuesday"]  
        wednesday =  request.data["wednesday"]  
        thursday = request.data["thursday"]  
        friday =  request.data["friday"] 
        print('2')
        start_hours_in = request.data["startHoursIn"]  
        end_hours_in = request.data["endHoursIn"]
        start_in = start_hours_in + ':00'
        end_in = end_hours_in+':00'
     #    start_in = datetime.strptime(start_hours_in,"%H:%M:%S")
     #    end_in = datetime.strptime(end_hours_in,"%H:%M:%S")
        if not Doctor.objects.filter(name=name).exists():
             section = Section.objects.get(name=section_name)
             doctor  = Doctor()
             doctor.name = name
             doctor.specialization = specialization
             doctor.description = description
             doctor.photo = image
             doctor.section = section
             # the days when doctor comes
             doctor.saturday =True if saturday=='1' else False
             doctor.sunday = True if sunday=='1' else False
             doctor.monday = True if monday=='1' else False
             doctor.tuesday = True if tuesday=='1' else False
             doctor.wednesday = True if wednesday=='1' else False
             doctor.thursday = True if thursday=='1' else False
             doctor.friday = True if friday=='1' else False
             #end days
             doctor.start_hours_in = start_in
             doctor.end_hours_in = end_in
             doctor.save()
             result = 'ok'
             return JsonResponse({
                  'result':result,
                  'message':'added successfuly'
             })
        else:
             return JsonResponse({
                  'result':result,
                  'message':' doctor '+ name +' already exists'
             })  
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })   
#-------------------------------------------------------------
################ API FOR GET DOCTOR DATAILS ##################
#-------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def doctor_information(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["name"]
        doctor = Doctor.objects.get(name=name)
        doctor_name = doctor.name
        doctor_section = doctor.section.name
        doctor_picture = doctor.photo.url
        doctor_description = desc_lines(doctor.description)
        saturday = '1' if doctor.saturday else '0'
        sunday = '1' if doctor.sunday else '0'
        monday= '1' if doctor.monday else '0'
        tuesday = '1' if doctor.tuesday else '0'
        wednesday = '1' if doctor.wednesday else '0'
        thursday ='1' if doctor.thursday else '0'
        friday ='1' if doctor.friday else '0'
        start_hours_in = doctor.start_hours_in.strftime("%H:%M")
        end_hours_in = doctor.end_hours_in.strftime("%H:%M")      
        result ='ok'
        return JsonResponse({
             'doctorName':doctor_name,
             'doctorSection':doctor_section,
             'doctorDesc':doctor_description,
             'doctorImage':doctor_picture,
             'saturday':saturday,
             'sunday':sunday,
             'monday':monday,
             'tuesday':tuesday,
             'wednesday':wednesday,
             'thursday':thursday,
             'friday':friday,
             'startHoursIn':start_hours_in,
             'endHoursIn':end_hours_in
        })
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })
#-------------------------------------------------------------
################ API FOR EDIT DOCTOR  ########################
#-------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def edit_doctor(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["doctorName"]
        image = request.POST.get('doctorImage',0)
        description = request.POST.get("description",0)
        section_name = request.POST.get("sectionName",0)
       
        spez = request.POST.get("Specialization",0)
        saturday = request.POST.get("saturday",0)
        sunday = request.POST.get("sunday",0)
        monday = request.POST.get("monday",0)
        tuesday = request.POST.get("tuesday",0)
        wednesday = request.POST.get("wednesday",0)
        thursday = request.POST.get("thursday",0)
        friday = request.POST.get("friday",0)
        start_in = request.POST.get("startHoursIn",0)
        end_in = request.POST.get("endHoursIn",0)

        doctor = Doctor.objects.get(name=name)

        if image != 0:
                doctor.photo = image        
        if saturday != 0:        
          doctor.saturday = True if saturday =='1' else False
        if sunday !=0:
          doctor.sunday =  True if sunday =='1' else False
        if monday !=0:
          doctor.monday =  True if monday =='1' else False
        if tuesday!=0:
          doctor.tuesday =  True if tuesday =='1' else False
        if wednesday !=0:
          doctor.wednesday =  True if wednesday =='1' else False
        if thursday !=0:
          doctor.thursday =  True if thursday =='1' else False
        if friday !=0 :
          doctor.friday =  True if friday =='1' else False
        if start_in !=0:
          start_in = start_in + ':00'
          doctor.start_hours_in = start_in
        if end_in !=0:
          end_in = end_in+':00'  
          doctor.end_hours_in = end_in
        if description !=0:
          doctor.description = description
        if spez !=0:
          doctor.specialization = spez
        if section_name !=0:
             section = Section.objects.get(name=section_name)
             doctor.section = section  
        doctor.save()
        result = 'ok'
        return JsonResponse({
                  'result':result,
                  'message':'edit successfuly'
             }) 
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })
#-------------------------------------------------------------
################ API FOR DELETE DOCTOR  ######################
#-------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def delete_doctor(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["doctorName"]
        doctor = Doctor.objects.get(name=name)
        doctor.delete()
        result = 'ok'
        return JsonResponse({
             'result':result,
             'message':'doctor deleted successfuly'
             
        })
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })
#-------------------------------------------------------------
############### API FOR THERAPIST INFORMATION ################
#-------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def therapist_information(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["name"]
        therapist = Therapist.objects.get(name=name)
        therapist_name = therapist.name
        therapist_section = therapist.section.name
        therapist_picture = therapist.photo.url
        therapist_description = desc_lines(therapist.description)
        saturday = '1' if therapist.saturday else '0'
        sunday = '1' if therapist.sunday else '0'
        monday= '1' if therapist.monday else '0'
        tuesday = '1' if therapist.tuesday else '0'
        wednesday = '1' if therapist.wednesday else '0'
        thursday ='1' if therapist.thursday else '0'
        friday ='1' if therapist.friday else '0'
        start_hours_in = therapist.start_hours_in.strftime("%H:%M")
        end_hours_in = therapist.end_hours_in.strftime("%H:%M")      
        result ='ok'
        return JsonResponse({
             'therapistName':therapist_name,
             'therapistSection':therapist_section,
             'therapistDesc':therapist_description,
             'therapistImage':therapist_picture,
             'saturday':saturday,
             'sunday':sunday,
             'monday':monday,
             'tuesday':tuesday,
             'wednesday':wednesday,
             'thursday':thursday,
             'friday':friday,
             'startHoursIn':start_hours_in,
             'endHoursIn':end_hours_in
        })
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })
#-------------------------------------------------------------
################ API FOR EDIT DOCTOR  ########################
#-------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def edit_therapist(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["therapistName"]
        image = request.POST.get('therapistImage',0)
        description = request.POST.get("description",0)
        section_name = request.POST.get("sectionName",0)
       
        spez = request.POST.get("spezialiation",0)
        saturday = request.POST.get("saturday",0)
        sunday = request.POST.get("sunday",0)
        monday = request.POST.get("monday",0)
        tuesday = request.POST.get("tuesday",0)
        wednesday = request.POST.get("wednesday",0)
        thursday = request.POST.get("thursday",0)
        friday = request.POST.get("friday",0)
        start_in = request.POST.get("startHoursIn",0)
        end_in = request.POST.get("endHoursIn",0)

        therapist = Therapist.objects.get(name=name)

        if image != 0:
                therapist.photo = image        
        if saturday != 0:        
          therapist.saturday = True if saturday =='1' else False
        if sunday !=0:
          therapist.sunday =  True if sunday =='1' else False
        if monday !=0:
          therapist.monday =  True if monday =='1' else False
        if tuesday!=0:
          therapist.tuesday =  True if tuesday =='1' else False
        if wednesday !=0:
          therapist.wednesday =  True if wednesday =='1' else False
        if thursday !=0:
          therapist.thursday =  True if thursday =='1' else False
        if friday !=0 :
          therapist.friday =  True if friday =='1' else False
        if start_in !=0:
          start_in = start_in + ':00'
          therapist.start_hours_in = start_in
        if end_in !=0:
          end_in = end_in+':00'  
          therapist.end_hours_in = end_in
        if description !=0:
          therapist.description = description
        if spez !=0:
          therapist.specialization = spez
        if section_name !=0:
             section = Section.objects.get(name=section_name)
             therapist.section = section  
        therapist.save()
        result = 'ok'
        return JsonResponse({
                  'result':result,
                  'message':'edit successfuly'
             }) 
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })
#-------------------------------------------------------------
################ API FOR DELETE DOCTOR  ######################
#-------------------------------------------------------------
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def delete_therapist(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        name = request.data["doctorName"]
        therapist = Therapist.objects.get(name=name)
        therapist.delete()
        result = 'ok'
        return JsonResponse({
             'result':result,
             'message':'doctor deleted successfuly'
             
        })
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })
#-------------------------------------------------------------
################ API FOR GET SECTIONS ########################
#-------------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def section_names(request):
     try:
        result = 'invalid'
        user = request.user
        if user.role != 'APPMANAGER':
              return JsonResponse({
                   'result':result,
                   'message':'you don\'t have permission to do this action'
              })
        all_section = Section.objects.all()
        names_list = []
        for sec in all_section:
            name = sec.name
            names_list.append(name)
        names_list.sort()
        result = 'ok'
        return JsonResponse({
             'result':result,
             'sections':names_list
         })
     except:
          return JsonResponse({
               'result':result,
               'message':'invalid or missing data',
          })     
          
          