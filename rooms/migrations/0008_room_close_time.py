# Generated by Django 3.2.9 on 2022-01-19 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0007_alter_room_craeted'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='close_time',
            field=models.DateTimeField(null=True),
        ),
    ]
