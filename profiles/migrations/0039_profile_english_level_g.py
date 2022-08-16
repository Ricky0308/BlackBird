# Generated by Django 3.2.9 on 2022-02-15 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0038_profile_certified'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='english_level_g',
            field=models.CharField(blank=True, choices=[('Begginer', 'Begginer'), ('Lower Intermediate', 'Lower Intermediate'), ('Intermediate', 'Intermediate'), ('Upper Intermediate', 'Upper Intermediate'), ('Advanced', 'Advanced'), ('Almost Native', 'Almost Native')], max_length=40, null=True),
        ),
    ]