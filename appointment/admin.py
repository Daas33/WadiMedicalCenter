from django.contrib import admin
from .models import Device,Doctor,Section,rate,Post,Therapist,Offer,doctor_appointment,device_appointment,Instruction

admin.site.register(Section)
admin.site.register(Device)
admin.site.register(Doctor)
admin.site.register(Therapist)
admin.site.register(rate)
admin.site.register(Post)
admin.site.register(Offer)
admin.site.register(Instruction)
admin.site.register(doctor_appointment)
admin.site.register(device_appointment)

