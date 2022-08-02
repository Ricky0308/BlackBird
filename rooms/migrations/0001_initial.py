# Generated by Django 3.2.9 on 2021-12-15 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0024_remove_profile_followers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('text', models.TextField(blank=True, help_text='Write the room descrption here!')),
                ('max_num', models.IntegerField(null=True)),
                ('craeted', models.DateTimeField(auto_now=True)),
                ('open_time', models.DateTimeField()),
                ('applicants', models.ManyToManyField(null=True, related_name='applicants', to='profiles.Profile')),
                ('owners', models.ManyToManyField(related_name='owners', to='profiles.Profile')),
                ('participants', models.ManyToManyField(null=True, related_name='participants', to='profiles.Profile')),
            ],
        ),
    ]