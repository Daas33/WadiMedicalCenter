# Generated by Django 4.1.7 on 2023-05-19 15:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0010_patientprofile_birth_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patientprofile",
            name="img",
            field=models.ImageField(
                blank=True,
                default="default_pic.jpg",
                null=True,
                upload_to="users_photos/%Y/%m/%d/",
            ),
        ),
    ]