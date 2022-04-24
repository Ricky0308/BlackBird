from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify 
import uuid
from .utils import get_random_code, tz_list
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify 

from rooms.utils import get_random_code
from bb2.lists import (COUNTRY_CHOICES, COUNTRY_LIST, SEX_CHOICES, 
	SEX_LIST, AGE_LIST,
	PUNCTUALITY_CHOICES, POLITENESS_CHIOCES, AGE_CHOICES, 
	ENGLISH_LEVEL_GENERAL_CHOICES, IELTS_SCORE_CHOICES, 
	TOEFL_SCORE_CHOICES, TAG_CHOICES, FOOTPRINT_CHOICES,
	PURPOSE_CHOICES)

import datetime

from collections import Iterable

# Create your models here.


class StringListField(models.TextField):
	description = 'A field for python lists'

	def __init__(self, valid_choices=None, *args, **kwargs):
		self.valid_choices = valid_choices
		super().__init__(*args, **kwargs)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		if self.valid_choices is not None:
			kwargs['valid_choices'] = self.valid_choices
		return name, path, args, kwargs

	def from_db_value(self, value, expression, connection):
		if value is None:
			return []
		return value.split(',')

	def check_valid_choices(self, values):
		for val in values:
			if not val in self.valid_choices:
					raise ValidationError(
						self.error_messages["invalid_choice"],
						code="invalid_choice",
						params={"value": val},
					)

	def to_python(self, value):
		if value is None:
			return 
		if isinstance(value, list):
			string = ''.join(map(lambda x: str(x), value))
			if ',' in string:
				raise ValidationError(_('items cannot contain a comma : from to_python'))
			return value
		val_list = value.split(',')
		return list(map(lambda x: x.strip(), val_list))

	def validate(self, values, model_instance):
		# check if every value in the value list is a valid choice 
		# raise ValidationError(_(f'{values}: from validate'))
		if not self.editable:
			return
		if self.valid_choices is not None and values not in self.empty_values:
			self.check_valid_choices(values)
		if values is None and not self.null:
			raise ValidationError(self.error_messages["null"], code="null")

		if not self.blank and values in self.empty_values:
			raise ValidationError(self.error_messages["blank"], code="blank")

				


	def get_prep_value(self, value):
		if not value:
			return 
		assert(isinstance(value, list))
		string = ''.join(map(lambda x: str(x), value))
		if ',' in string:
			raise ValidationError(_('items cannot contain a comma : from get_prep_value'))
		return ','.join(value)

	def value_from_object(self, obj):
		value = getattr(obj, self.attname)
		if not value:
			return 
		return ','.join(value)


class MultipleChoiceableCharField(models.CharField):
	# allows using MultipleChoiceField for form
	# but chosing only onw value is allowed
	# raise ValidationError(_('Unreasonable error : from MultipleChoiceableCharField to_python'))
	def to_python(self, value):
		if isinstance(value, (list, tuple)):
			if len(value) > 1:
				raise ValidationError(_('only one value is allowed'))
			elif len(value) == 0:
				return 
			else:
				value = value[0]
		return super().to_python(value)
		# 	raise ValidationError(_(f'{value}: from validate'))
		
	

class Profile(models.Model):
	id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(default="no bio...", max_length=10000)
	country = models.CharField(choices=COUNTRY_CHOICES, max_length=200, blank=False)
	sex = models.CharField(choices=SEX_CHOICES, max_length=10, blank=True, null=True)
	age = models.CharField(choices=AGE_CHOICES, max_length=20, blank=True, null=True)
	english_level_g = models.CharField(choices=ENGLISH_LEVEL_GENERAL_CHOICES, max_length=40, blank=True, null=True)
	timezone = models.CharField(choices=tz_list, max_length=200, blank=True)
	auto_timezone = models.BooleanField(default=True)
	avatar = models.ImageField(default="avatar.png", null=False, upload_to="avatars/")
	follow = models.ManyToManyField(User, blank=True, related_name='follow')
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	purpose = models.CharField(
		default='conversation practice',
		max_length=50,
		choices=PURPOSE_CHOICES,
	)

	# pre-approved 
	next_country = models.CharField(choices=COUNTRY_CHOICES, max_length=200, blank=True, null=True)
	next_sex = models.CharField(choices=SEX_CHOICES, max_length=10, blank=True, null=True)
	next_age = models.CharField(choices=AGE_CHOICES, max_length=20, blank=True, null=True)
	next_toefl = models.CharField(choices=TOEFL_SCORE_CHOICES, max_length=200, blank=True, null=True)
	next_ielts = models.CharField(choices=IELTS_SCORE_CHOICES, max_length=200, blank=True, null=True)
	next_country_reason = models.TextField(default=None, max_length=1000, null=True, blank=True)
	next_sex_reason = models.TextField(default=None, max_length=1000, null=True, blank=True)
	next_age_reason = models.TextField(default=None, max_length=1000, null=True, blank=True)


	# English level
	toefl = models.CharField(choices=TOEFL_SCORE_CHOICES, max_length=200, blank=True, null=True)
	ielts = models.CharField(choices=IELTS_SCORE_CHOICES, max_length=200, blank=True, null=True)
	certification_toefl = models.ImageField(default='no_certification.png', blank=True, null=False, upload_to="certifications/")
	certification_ielts = models.ImageField(default='no_certification.png', blank=True, null=False, upload_to="certifications/")

	certified = models.BooleanField(default=False, null=True)

	def save(self, *args, **kwargs):
		if not self.id:
			same_id = len(Profile.objects.filter(id = self.id))
			while same_id > 1:
				self.id = uuid.UUID(str(uuid.uuid4()))
				same_id = len(Profile.objects.filter(id = self.id))
		super().save(*args, **kwargs)

	def make_uid(self):
		return urlsafe_base64_encode(force_bytes(self.id))



	def personal_info(self):
		info = [self.country, self.sex, 
		self.age,]
		if self.toefl is not None:
			info += ['TOEFL '+str(self.toefl)]
		if self.ielts is not None:
			info += ['IELTS '+str(self.ielts)]
		return [i for i in info if i is not None] 

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Target(models.Model):
	profile = models.OneToOneField(
		Profile, 
		on_delete=models.CASCADE
	)
	country = StringListField(
		valid_choices = COUNTRY_LIST,
		blank=True, 
		null=True,
	)
	sex = StringListField(
		valid_choices = SEX_LIST,
		blank=True, 
		null=True
	)
	age = StringListField(
		valid_choices = AGE_LIST,
		blank=True, 
		null=True,
	)
	def __str__(self):
		return f'{self.profile}'

	def make_dict(self):
		# customized model_to_dict() 
		field_names = [x.name for x in Target._meta.fields]
		return {x:getattr(self, x) for x in field_names}

	def value_list(self):
		# return a generator containing all values except for id and profile
		exclude = ['id', 'profile']
		field_names = [x.name for x in Target._meta.fields if x.name not in exclude]
		tmp_value_list = [getattr(self, x) for x in field_names]
		for value in tmp_value_list:
			if isinstance(value, Iterable):
				for elem in value:
					yield elem
			else:
				yield str(value)




class Tag(models.Model):
	name = models.CharField(max_length = 100)
	profiles = models.ManyToManyField(
		Profile, 
		blank=True, 
		related_name='tags'
	)
	kind = models.CharField(
		max_length = 100, 
		choices=TAG_CHOICES
	)

	def __str__(self):
		return f'{self.id} {self.kind} ({self.name})'


class Review(models.Model):
	slug = models.SlugField(
		unique=True, 
		blank=True
	)
	reviewee = models.ForeignKey(
		Profile, 
		related_name='reviewee', 
		on_delete=models.CASCADE
	)
	reviewer = models.ForeignKey(
		Profile, 
		related_name='reviewer', 
		on_delete=models.CASCADE
	)
	review_title = models.CharField(
		max_length=100, 
		blank=True
	)
	review_text = models.TextField(
		max_length=1000, 
		blank=True
	)
	warning_title = models.CharField(
		max_length=100, 
		blank=True, 
		null=True
	)
	warning_text = models.TextField(
		max_length=1000, 
		null=True, 
		blank=True
	)
	punctuality = models.CharField(
		choices=PUNCTUALITY_CHOICES, 
		max_length=100, 
		blank=True, 
		null=True
	)
	politeness = models.CharField(
		choices=POLITENESS_CHIOCES, 
		max_length=100, 
		blank=True, 
		null=True
	)
	created = models.DateTimeField(auto_now_add=True)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def save(self, *args, **kwargs):
		if not self.slug:
			to_slug = self.reviewee.first_name.lower()
			num = len(Review.objects.filter(slug=to_slug))
			while num >= 1:
				to_slug = slugify(to_slug + ' ' + str(get_random_code()))
				num = len(Review.objects.filter(slug=to_slug))
			self.slug = to_slug
		super().save(*args, **kwargs)

	def __str__(self):
		is_warning = ['', '( !! ) '][bool(self.warning_title)]
		data_format = '%m/%d %H:%M'
		created = datetime.datetime.strftime(self.created, data_format)
		return f'{is_warning}{self.reviewer.first_name} -> {self.reviewee.first_name} ({created})'



class Footprint(models.Model):
	profile = models.ForeignKey(
		Profile, 
		related_name='footprints', 
		on_delete=models.CASCADE,
		blank=True,
		null = True,
	)
	created = models.DateTimeField(auto_now_add = True)
	kind = models.CharField(
		max_length=50, 
		choices=FOOTPRINT_CHOICES,
		null = True,
	)
	profile_page = models.ForeignKey(
		Profile, 
		related_name='page_views', 
		on_delete=models.CASCADE,
		blank=True,
		null = True,
	)
	room_page = models.ForeignKey(
		'rooms.Room', 
		related_name='page_views', 
		on_delete=models.CASCADE,
		blank=True,
		null = True,
	)

	def __str__(self):
		data_format = '%m/%d %H:%M'
		created = datetime.datetime.strftime(self.created, data_format)
		return F'({self.id}) {self.profile} : {self.kind} : {created}'



