# Generated by Django 4.1.7 on 2023-04-22 21:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "appointment",
            "0015_alter_doctor_membership_date_alter_offer_ending_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 23, 0, 2, 16, 860579)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="ending_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 23, 0, 2, 16, 859550)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 23, 0, 2, 16, 859550)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="publish_date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name="therapist",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 23, 0, 2, 16, 860579)
            ),
        ),
    ]
