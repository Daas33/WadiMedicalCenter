# Generated by Django 4.1.7 on 2023-04-13 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointment", "0009_alter_device_appointment_attended_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 13, 17, 23, 37, 565654)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="ending_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 13, 17, 23, 37, 565654)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 13, 17, 23, 37, 565654)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 13, 17, 23, 37, 564784)
            ),
        ),
        migrations.AlterField(
            model_name="therapist",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 13, 17, 23, 37, 566651)
            ),
        ),
    ]
