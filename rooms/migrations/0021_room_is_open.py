# Generated by Django 3.2.9 on 2022-02-18 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0020_remove_room_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_open',
            field=models.BooleanField(default=False),
        ),
    ]
