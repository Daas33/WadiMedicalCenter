from django.urls import path
from . import views


urlpatterns =[
    path('get_doctor_image',views.get_doctor_image,name='get_doctor_image'),
    path('home_page/',views.home_page,name='home_page'),
    path('offers/',views.offers,name='offers'),
    #personal information
    path('profile_info',views.profile_info,name='profile_info'),
    #edit
    #doctor appointments and info   
    path('doctor_info',views.doctor_info,name='doctor_info'),
    path('doctor_schedule',views.doctor_schedule,name='doctor_schedule'),
    path('reserve_doctor_appointment',views.reserve_doctor_appointment,name='reserve_doctor_appointment'),

]