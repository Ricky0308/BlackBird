# Generated by Django 3.2.9 on 2022-01-16 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0026_rename_tz_profile_my_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='auto_timezone',
            field=models.BooleanField(default=True),
        ),
    ]
