# Generated by Django 4.1.7 on 2023-04-21 17:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "appointment",
            "0012_alter_doctor_membership_date_alter_offer_ending_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 21, 20, 45, 35, 985171)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="ending_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 21, 20, 45, 35, 985171)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 21, 20, 45, 35, 985171)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="publish_date",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="therapist",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 21, 20, 45, 35, 986194)
            ),
        ),
    ]