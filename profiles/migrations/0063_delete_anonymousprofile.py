# Generated by Django 3.2.9 on 2022-03-11 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0025_alter_room_open_time'),
        ('profiles', '0062_anonymousprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AnonymousProfile',
        ),
    ]
