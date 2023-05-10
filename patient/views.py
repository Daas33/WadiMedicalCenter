from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view,permission_classes
from datetime import datetime,date,timedelta,time
from appointment.models import Post,Instruction,Offer,Doctor,Device,Therapist
from account.models import Patient
from account.models import PatientProfile
import json
import calendar
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
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
############## API FOR ####################################
#----------------------------------------------------------
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def a(request):
     result = 'invalid'
     try:
          pass
     except:
          pass
