from django.urls import path
from . import views


urlpatterns =[
        path( 'today_appointments',views.today_appointments ,name='today_appointments'),
        path('Doctors',views.Doctors ,name='Doctors'),
        path('not_attend_appointment',views.not_attend_appointment,name='not_attend_appointment'),
        path('attend_appointment',views.attend_appointment,name='attend_appointment'),
        path('see_schedule',views.see_schedule,name='see_schedule'),
        path('Devices',views.Devices,name='Devices'),
        path('delete_appointment',views.delete_appointment,name='delete_appointment'),
        path('edit_appointment',views.edit_appointment,name='edit_appointment'),
        path('add_doctor_appointment',views.add_doctor_appointment,name='add_doctor_appointment'),
        path('Patients',views.Patients,name='Patients'),
        path('add_patient',views.add_patient,name='add_patient'),
        path('patient_appointments',views.patient_appointments,name='patient_appointments'),
        path('device_reserved_appointments',views.device_reserved_appointments,name = 'device_reserved_appointments'),
        path('available_dt_appointments',views.available_dt_appointments,name='available_dt_appointments'),
        path('add_device_appointment',views.add_device_appointment,name='add_device_appointment'),
        path('therapists_names',views.therapists_names,name='therapists_names'),
        path('patient_info',views.patient_info,name='patient_info'),
        path('edit_patient',views.edit_patient,name='edit_patient'),
        ]