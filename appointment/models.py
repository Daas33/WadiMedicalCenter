from django.db import models
from datetime import datetime
from account.models import User,Patient
from django.utils import timezone

class Section(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="posts_photos/%Y/%m/%d/",null=True,blank=True)

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
    discount = models.DecimalField(blank=True,null=True,max_digits=2,decimal_places=2)


    

class Doctor(models.Model):
    #the name of the doctor and the study specialization and description is some details and expert pf the doctor
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    photo = models.ImageField(upload_to="employee_photos/%Y/%m/%d/",null=True,blank=True)
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
    rate = models.IntegerChoices('rete','1 2 3 4 5')
    



    
class Therapist(models.Model):
    #the name of the therapist and the study specialization and description is some details and expert pf the doctor
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    photo = models.ImageField(upload_to="employee_photos/%Y/%m/%d/",null=True,blank=True)
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
    rate = models.IntegerChoices('rete','1 2 3 4 5')

class Device(models.Model):
    name = models.CharField(max_length=255)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    photo = models.ImageField(upload_to="devices_photos/%Y/%m/%d/",null=True,blank=True)
    active = models.BooleanField(default=True)



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
    reception_rate = models.IntegerChoices('reception','1 2 3 4 5')
    cleanless = models.IntegerChoices('cleanless','1 2 3 4 5')
    treatment_od_medical_staff =models.IntegerChoices('treatment_of_medical_staff','1 2 3 4 5')
    therapisting_rate =  models.IntegerChoices('therapisting_rate','1 2 3 4 5')
    name_of_th_therapist = models.CharField(max_length=255)