from xml.dom import ValidationErr
from attr import fields
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from importlib_metadata import email
from .models import Profile, Tag, Target
from django.forms import ModelForm
from django import forms
from django.forms import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from bb2.lists import COUNTRY_CHOICES, AGE_CHOICES, SEX_CHOICES, TAG_LIST

class CustomMultipleModelChoiceField(forms.ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		return f'{obj.name}'

class ProfileCreationForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = [
			'first_name', 
			'last_name', 
			'country', 
		]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['last_name'].required = False



class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['first_name', 
			'last_name', 
			'bio', 
			'english_level_g',
			'timezone',
			'avatar',
			'next_country',
			'next_sex',
			'next_age',
			'next_toefl',
			'next_ielts',
			'certification_toefl',
			'certification_ielts',
			'next_country_reason',
			'next_sex_reason',
			'next_age_reason'
			]

	avatar = certification_toefl = certification_ielts = forms.ImageField(widget=forms.FileInput)

class PurposeForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['purpose']
		widgets={}

class EfficientMetaclass(models.DeclarativeFieldsMetaclass):
	def __new__(mcs, name, bases, attrs):
		for x in TAG_LIST:
			attrs[x.lower()] = CustomMultipleModelChoiceField(
				required=False,
				widget=forms.CheckboxSelectMultiple(), 
				queryset=Tag.objects.filter(kind=x).order_by('name')
			)
		return super().__new__(mcs, name, bases, attrs)

class TagForm(forms.Form, metaclass=EfficientMetaclass):
	'''
	fields are created automatically via EfficientMetaclass
	'''
	
class TargetForm(forms.ModelForm):
	class Meta:
		model = Target
		exclude = ['profile']
		widgets = {}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		available_countries = set(map(lambda x : x.country, Profile.objects.all()))
		AVA_COUNTRY_CHOICES = sorted(
			[[x, x] for x in available_countries], 
			key=lambda x: x[0])
		fields_and_choices = (
			('country', AVA_COUNTRY_CHOICES),
			('age', AGE_CHOICES),
			('sex', SEX_CHOICES),
		)
		for field, choice in fields_and_choices:
			self.fields[field] = forms.MultipleChoiceField(
				required=False, 
				widget=forms.CheckboxSelectMultiple(), 
				choices=choice,
			)
		



class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField()


class EmailAuthenticationForm(AuthenticationForm):
	email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'black-input'}))
	username = UsernameField(required=False, widget=forms.TextInput(attrs={"autofocus": True})) 

	error_messages = {
		"invalid_login": _(
			"email address and password don't match."
		),
		"inactive": _("This account is inactive."),
	}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password'].widget.attrs.update({'class':'black-input'})

	def get_invalid_login_error(self):
		return ValidationError(
			self.error_messages["invalid_login"],
            code="invalid_login",
		)

	def clean(self):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')

		if email is not None and password:
			from bb2.authentication import authenticate
			self.user_cache = authenticate(
				self.request, email = email, password = password
			)
			if self.user_cache is None:
				raise self.get_invalid_login_error()
			else:
				self.confirm_login_allowed(self.user_cache)
		
		return self.cleaned_data

	



class MyForm(forms.Form):
	a_filed = forms.EmailField(
		widget=forms.EmailInput(
			attrs={'class':'black-input'}))
