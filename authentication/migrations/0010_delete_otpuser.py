# Generated by Django 4.2.7 on 2023-11-16 09:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0009_otpuser"),
    ]

    operations = [
        migrations.DeleteModel(
            name="OTPUser",
        ),
    ]
