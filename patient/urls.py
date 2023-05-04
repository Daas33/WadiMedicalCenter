from django.urls import path
from . import views


urlpatterns =[
    path('get_doctor_image',views.get_doctor_image,name='get_doctor_image'),
    path('home_page/',views.home_page,name='home_page'),
    path('offers/',views.offers,name='offers'),
    # path('add_post',views.add_post,name='add_post'),
   

]