# Generated by Django 3.2.9 on 2022-02-18 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0019_auto_20220216_0517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='is_open',
        ),
    ]