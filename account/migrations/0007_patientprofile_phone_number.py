# Generated by Django 4.1.7 on 2023-03-27 15:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0006_patientprofile_file_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="patientprofile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
