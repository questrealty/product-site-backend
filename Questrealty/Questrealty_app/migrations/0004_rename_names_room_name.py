# Generated by Django 3.2 on 2022-07-19 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Questrealty_app', '0003_auto_20220719_0856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='names',
            new_name='name',
        ),
    ]
