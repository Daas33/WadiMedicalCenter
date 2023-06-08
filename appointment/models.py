from django.db import models
from datetime import datetime
from account.models import User,Patient
from django.utils import timezone


class rateValues(models.IntegerChoices):
    ONE = 1 , "Very Bad"
    TWO = 2 , "Bad"
    THREE = 3 , "Normal"
    FOUR = 4 , "High"
    FIVE = 5 , "Very High"


class Section(models.Model):
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255,blank=True,null=True)
    photo = models.ImageField(upload_to="posts_photos/%Y/%m/%d/",null=True,blank=True,default='default_sec.png')

class Post(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    photo = models.ImageField(upload_to="posts_photos/%Y/%m/%d/",null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    publish_date = models.DateTimeField()

class Instruction(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    photo = models.ImageField(upload_to="posts_photos/%Y/%m/%d/",null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    
class Offer(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    photo = models.ImageField(upload_to="posts_photos/%Y/%m/%d/",null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    publish_date = models.DateTimeField(blank=True,null=True)
    ending_date = models.DateTimeField(blank=True,null=True)
    old_price = models.IntegerField(blank=True,null=True)
    new_price = models.IntegerField(blank=True,null=True)
    discount = models.IntegerField(blank=True,null=True)


    

class Doctor(models.Model):
    #the name of the doctor and the study specialization and description is some details and expert pf the doctor
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    photo = models.ImageField(upload_to="employee_photos/%Y/%m/%d/",null=True,blank=True,default='default_pic.jpg')
    #----------------------------------------------------------
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    membership_date = models.DateTimeField(auto_now_add=True)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    start_hours_in = models.TimeField()
    end_hours_in = models.TimeField()
    rate = models.IntegerField(choices=rateValues.choices,null=True,blank =True)
    



    
class Therapist(models.Model):
    #the name of the therapist and the study specialization and description is some details and expert pf the doctor
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    photo = models.ImageField(upload_to="employee_photos/%Y/%m/%d/",null=True,blank=True,default='default_pic.jpg')
    #----------------------------------------------------------
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    membership_date = models.DateTimeField(auto_now_add=True)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    monday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    start_hours_in = models.TimeField()
    end_hours_in = models.TimeField()
    rate = models.IntegerField(choices=rateValues.choices,null=True,blank =True)

class Device(models.Model):
    name = models.CharField(max_length=255)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    photo = models.ImageField(upload_to="devices_photos/%Y/%m/%d/",null=True,blank=True,default='default_dev.jpg')
    active = models.BooleanField(default=True)
    is_service = models.BooleanField(default=False)



#--------------------------------------------------------


class doctor_appointment(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    attended = models.BooleanField(default=True)

    #dateti = models.DateTimeField()
#----------------------------------------------------------
class device_appointment(models.Model):
    therapist = models.ForeignKey(Therapist,on_delete=models.CASCADE)
    device = models.ForeignKey(Device,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    attended = models.BooleanField(default=True)


#------------------------------------------------------------
class rate(models.Model):
    #every rate is based on 5 stars
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    doctor_appointment = models.ForeignKey(doctor_appointment, on_delete=models.CASCADE,blank=True,null=True)
    device_appointment = models.ForeignKey(device_appointment, on_delete=models.CASCADE,blank=True,null=True)
    reception_rate = models.IntegerField(choices=rateValues.choices,null=True,blank =True)
    cleanless = models.IntegerField(choices=rateValues.choices,null=True,blank =True)
    treatment_od_medical_staff =models.IntegerField(choices=rateValues.choices,null=True,blank =True)
    therapisting_rate =  models.IntegerField(choices=rateValues.choices,null=True,blank =True)
    name_of_th_therapist = models.CharField(max_length=255)