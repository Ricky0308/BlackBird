# Generated by Django 3.2.9 on 2022-02-12 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0012_rename_appliable_room_joinable'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(default='default_room_image.png', upload_to='room_images/'),
        ),
    ]
