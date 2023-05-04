# Generated by Django 4.1.7 on 2023-03-29 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "appointment",
            "0004_alter_doctor_membership_date_alter_offer_ending_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 29, 16, 42, 21, 815459)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="ending_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 29, 16, 42, 21, 815459)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 29, 16, 42, 21, 815459)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 29, 16, 42, 21, 814426)
            ),
        ),
        migrations.AlterField(
            model_name="therapist",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 29, 16, 42, 21, 815459)
            ),
        ),
    ]