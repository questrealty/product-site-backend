# Generated by Django 4.1 on 2022-09-02 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="newuser", name="signup_date",),
    ]
