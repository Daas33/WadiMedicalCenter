from django.urls import path
from . import views
from appointment import views as av


urlpatterns =[
    path('add_post',views.add_post,name='add_post'),
    path('add_ins',views.add_ins,name='add_ins'),
    #--------------------------------------------------
    path('doctors_therapists',views.doctors_therapists,name='doctors_therapists'),
    # ADD, EDIT, DELETE  A DOCTOR
    path('add_doctor',views.add_doctor,name='add_doctor'),
    path('doctor_information',views.doctor_information,name='doctor_information'),
    path('edit_doctor',views.edit_doctor,name='edit_doctor'),
    path('delete_doctor',views.delete_doctor,name='delete_doctor'),
    #--------------------------------------------------------
    # ADD, EDIT AND DELETE A THERAPIST
    path('add_therapist',views.add_therapist,name='add_therapist'),
    path('therapist_information',views.therapist_information,name='therapist_information'),
    path('edit_therapist',views.edit_therapist,name='edit_therapist'),
    path('delete_therapist',views.delete_therapist,name='delete_therapist'),
    #--------------------------------------------------
    path('devices',av.Devices,name='devices'),
    # ADD , EDIT AND  DELETE  A DEVICE
    path('add_device',views.add_device,name='add_device'),
    path('edit_device',views.edit_device,name ='edit_device'),
    path('device_information',views.device_information,name='device_information'),
    path('delete_device',views.delete_device,name='delete_device'),
    #----------------------------------------------------
    # GET SECTIONS ,ADD, EDIT  AND DEIETE A SECTION
    path('section_names',views.section_names,name='section_names'),
    path('add_section',views.add_section,name='add_section'),
    #-------------------------------------------------------
    # GET OFFERS , ADD, EDIT AND DELETE OFFER
    path('add_offer',views.add_offer,name='add_offer'),  
    
    
]