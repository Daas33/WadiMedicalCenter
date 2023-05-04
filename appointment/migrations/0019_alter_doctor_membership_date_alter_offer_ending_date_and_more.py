# Generated by Django 4.1.7 on 2023-04-26 11:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "appointment",
            "0018_alter_doctor_membership_date_alter_offer_ending_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 26, 14, 22, 32, 925401)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="ending_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 26, 14, 22, 32, 925401)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 26, 14, 22, 32, 925401)
            ),
        ),
        migrations.AlterField(
            model_name="therapist",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 26, 14, 22, 32, 926399)
            ),
        ),
    ]
