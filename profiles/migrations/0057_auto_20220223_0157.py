# Generated by Django 3.2.9 on 2022-02-23 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0056_auto_20220223_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='certification_ielts',
            field=models.ImageField(blank=True, default='no_certification.png', upload_to='certifications/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='certification_toefl',
            field=models.ImageField(blank=True, default='no_certification.png', upload_to='certifications/'),
        ),
    ]