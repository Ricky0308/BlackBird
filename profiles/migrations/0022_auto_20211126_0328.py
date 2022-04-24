# Generated by Django 3.2.9 on 2021-11-26 03:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0021_rename_d_id_profile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dummy_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
