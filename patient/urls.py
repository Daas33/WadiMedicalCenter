from django.urls import path
from . import views


urlpatterns =[
    path('get_doctor_image',views.get_doctor_image,name='get_doctor_image'),
    path('home_page/',views.home_page,name='home_page'),
    path('offers/',views.offers,name='offers'),
    #personal information
    path('profile_info',views.profile_info,name='profile_info'),
    path('notifications',views.notifications,name='notifications'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('my_appointments',views.my_appointments,name='my_appointments'),
    # sections  and objects in sections
    path('categories',views.categories,name='categories'),
    #######doctors section detils
    path('doctors_in_section',views.doctors_in_section,name='doctors_in_section'),
    #######devices section detils
    path('devices_in_section',views.devices_in_section,name='devices_in_section'),
    # get device or services appointments and info
    path('device_info',views.device_info,name='device_info'),
    path('device_therapists',views.device_therapists,name='device_therapists'),
    path('therapist_schedule',views.therapist_schedule,name='therapiast_schedule'),
    path('therapist_info',views.therapist_info,name='therapist_info'),
    path('reserve_device_appointment',views.reserve_device_appointment,name='reserve_device_appointment'),
    # get doctor appointments and info   
    path('doctor_info',views.doctor_info,name='doctor_info'),
    path('doctor_schedule',views.doctor_schedule,name='doctor_schedule'),
    path('reserve_doctor_appointment',views.reserve_doctor_appointment,name='reserve_doctor_appointment'),
    # path('section',views.section,name='section'),
    path('rate_appointment',views.rate_appointment,name='rate_appointment'),
]