# Generated by Django 4.1.7 on 2023-03-23 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0003_appmanager_manager_recertion"),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")], max_length=50
                    ),
                ),
                (
                    "relationship",
                    models.CharField(
                        choices=[("S", "Single"), ("M", "Married")], max_length=50
                    ),
                ),
                (
                    "img",
                    models.ImageField(
                        blank=True, null=True, upload_to="users_photos/%Y/%m/%d/"
                    ),
                ),
                (
                    "finger_print",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]