# Generated by Django 4.1.7 on 2023-04-28 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointment", "0022_device_photo"),
    ]

    operations = [
        migrations.AddField(
            model_name="device",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]