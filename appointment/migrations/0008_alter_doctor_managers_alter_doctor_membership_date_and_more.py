# Generated by Django 4.1.7 on 2023-04-02 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "appointment",
            "0007_alter_doctor_managers_rename_sanday_doctor_saturday_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="doctor",
            managers=[],
        ),
        migrations.AlterField(
            model_name="doctor",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 2, 14, 56, 39, 195781)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="ending_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 2, 14, 56, 39, 195781)
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 2, 14, 56, 39, 195781)
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="publish_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 2, 14, 56, 39, 194589)
            ),
        ),
        migrations.AlterField(
            model_name="therapist",
            name="membership_date",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 2, 14, 56, 39, 195781)
            ),
        ),
    ]
