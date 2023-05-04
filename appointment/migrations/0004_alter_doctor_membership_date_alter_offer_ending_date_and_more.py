# Generated by Django 4.1.7 on 2023-03-27 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointment", "0003_alter_doctor_membership_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 27, 17, 13, 45, 411896)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="ending_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 27, 17, 13, 45, 411896)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 27, 17, 13, 45, 411896)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 27, 17, 13, 45, 410898)
            ),
        ),
        migrations.AlterField(
            model_name="therapist",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 3, 27, 17, 13, 45, 411896)
            ),
        ),
    ]
