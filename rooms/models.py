import uuid

from django.db import models
from django.template.defaultfilters import slugify 
from django.core.validators import MaxValueValidator, MinValueValidator

from .utils import get_random_code


# Create your models here.




class Room(models.Model):
	name = models.CharField(max_length = 50, blank=False)
	slug = models.SlugField(unique=True, blank=True)
	text = models.TextField(blank=True, help_text='Write the room descrption here!')
	max_num = models.IntegerField(null=True, blank=True, choices=[(x, x) for x in range(2, 100)])
	craeted = models.DateTimeField(auto_now_add=True)
	joinable = models.BooleanField(default=True)
	no_apply = models.BooleanField(default=False)
	reveal_owner = models.BooleanField(default=True)
	image = models.ImageField(blank=True, null=True, default="default_room_image.png", upload_to="room_images/")

	# schedule 
	open_time = models.DateTimeField(null=True, blank=True)
	close_time = models.DateTimeField(null=True)
	is_open = models.BooleanField(default=False)

	# def limit_invited_choices(self):
	# 	return {'pk__in':self.owner.follow.all()}

	# involved people 
	owner = models.ForeignKey('profiles.Profile', related_name='owner', on_delete=models.CASCADE)
	invited = models.ManyToManyField('profiles.Profile', related_name='invited', blank=True)#, limit_choices_to={'pk__in':self.owner.follow.all()})
	applicants = models.ManyToManyField('profiles.Profile', related_name='applicants', blank=True)
	participants = models.ManyToManyField('profiles.Profile', related_name='participants', blank=True)

	def __str__(self):
		return self.name

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def save(self, *args, **kwargs):
		if not self.slug:
			to_slug = slugify(self.name)
			num = len(Room.objects.filter(slug=to_slug))
			while num >= 1:
				to_slug = slugify(to_slug + ' ' + str(get_random_code()))
				num = len(Room.objects.filter(slug=to_slug))
			self.slug = to_slug
		super().save(*args, **kwargs)

	def parent(self):
		return 'Room'



	



