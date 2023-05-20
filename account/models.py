from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        APPMANAGER = "APPMANAGER", "AppManager"
        RECEPTION = "RECEIPTION", "Reception"
        PATIENT = "PATIENT", "Patient"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


# --------------------------------------------------------------
# here the PATIENT MODELS
class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PATIENT)


class Patient(User):
    base_role = User.Role.PATIENT
    patient = PatientManager()

    class Meta:
        proxy = True

    def __str__(self):
        return self.username    


@receiver(post_save, sender=Patient)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "PATIENT":
        PatientProfile.objects.create(user=instance)


@receiver(post_save, sender=Patient)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance.role == "PATIENT":
        Token.objects.create(user=instance)

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file_number = models.IntegerField(null=True,blank=True)
    GENDER = (("M", "Male"), ("F", "Female"))
    RELATIONSHIP = (("S", "Single"), ("M", "Married"))
    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP, null=True, blank=True)
    img = models.ImageField(upload_to="users_photos/%Y/%m/%d/", null=True, blank=True,default='default_pic.jpg')
    finger_print = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255,blank=True,null=True)
    code = models.IntegerField(blank=True,null=True)
    birth_date = models.DateField(blank=True,null=True)

    def __str__(self):
            return self.user.username


# --------------------------------------------------------------
# here the RECEPTION MODELS
class ReceptionManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.RECEPTION)


class Reception(User):
    base_role = User.Role.RECEPTION
    reception = ReceptionManager()

    class Meta:
        proxy = True


@receiver(post_save, sender=Reception)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance.role == "RECEIPTION":
        Token.objects.create(user=instance)

# --------------------------------------------------------------
# here the MANAGER MODELS
class ManagerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.MANAGER)


class Manager(User):
    base_role = User.Role.MANAGER
    manager = ManagerManager()

    class Meta:
        proxy = True


@receiver(post_save, sender=Manager)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance.role == "MANAGER":
        Token.objects.create(user=instance)

# --------------------------------------------------------------
# here the APPMNAGER MODELS
class AppManagerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.APPMANAGER)


class AppManager(User):
    base_role = User.Role.APPMANAGER
    appmanager = AppManagerManager()

    class Meta:
        proxy = True

@receiver(post_save, sender=AppManager)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created and instance.role == "APPMANAGER":
        Token.objects.create(user=instance)        
#-----------------------------------------------------------------
######### GENERATE TOKEN FOR EVERY USER REGESTIRED ###############
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)