from django.contrib import admin
from .models import User,Patient,AppManager,Manager,PatientProfile,Reception
# Register your models here.
admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Reception)
admin.site.register(AppManager)
admin.site.register(Manager)
admin.site.register(PatientProfile)