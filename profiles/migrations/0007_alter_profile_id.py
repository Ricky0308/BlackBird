# Generated by Django 3.2.9 on 2021-11-25 04:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=True),
        ),
    ]