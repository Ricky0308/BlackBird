# Generated by Django 3.2.9 on 2022-01-27 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0011_auto_20220127_0351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='appliable',
            new_name='joinable',
        ),
    ]