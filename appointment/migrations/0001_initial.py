# Generated by Django 4.1.7 on 2023-03-24 16:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Instruction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="posts_photos/%Y/%m/%d/"
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Offer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="posts_photos/%Y/%m/%d/"
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "publish_date",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 3, 24, 18, 23, 58, 277256)
                    ),
                ),
                (
                    "ending_date",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 3, 24, 18, 23, 58, 277256)
                    ),
                ),
                ("old_price", models.IntegerField(blank=True, null=True)),
                ("new_price", models.IntegerField(blank=True, null=True)),
                (
                    "discount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=2, null=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="posts_photos/%Y/%m/%d/"
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "publish_date",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 3, 24, 18, 23, 58, 276258)
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="posts_photos/%Y/%m/%d/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Therapist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("specialization", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="employee_photos/%Y/%m/%d/"
                    ),
                ),
                (
                    "membership_date",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 3, 24, 18, 23, 58, 278289)
                    ),
                ),
                ("satrday", models.BooleanField(default=False)),
                ("sanday", models.BooleanField(default=False)),
                ("monday", models.BooleanField(default=False)),
                ("thursday", models.BooleanField(default=False)),
                ("wedensday", models.BooleanField(default=False)),
                ("tuesday", models.BooleanField(default=False)),
                ("friday", models.BooleanField(default=False)),
                ("start_hours_in", models.TimeField()),
                ("end_hours_in", models.TimeField()),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointment.section",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("specialization", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="employee_photos/%Y/%m/%d/"
                    ),
                ),
                (
                    "membership_date",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 3, 24, 18, 23, 58, 277256)
                    ),
                ),
                ("satrday", models.BooleanField(default=False)),
                ("sanday", models.BooleanField(default=False)),
                ("monday", models.BooleanField(default=False)),
                ("thursday", models.BooleanField(default=False)),
                ("wedensday", models.BooleanField(default=False)),
                ("tuesday", models.BooleanField(default=False)),
                ("friday", models.BooleanField(default=False)),
                ("start_hours_in", models.TimeField()),
                ("end_hours_in", models.TimeField()),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointment.section",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("active", models.BooleanField(default=True)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appointment.section",
                    ),
                ),
            ],
        ),
    ]
