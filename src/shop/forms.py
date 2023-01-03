from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django import forms

class MyUserCreationForm(UserCreationForm):
	class Meta:
		model = User
		fields = [ 'email', 'username', 'password1', 'password2']


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']

PAYMENT_CHOICES = (
	('FA', 'from account'),
	('CC', 'credit card'),
)


class CheckoutForm(forms.Form):
	street_address = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':"123 Street",
		'class': 'form-control'
		}))
	apartment_address = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':"apartment",
		'class': 'form-control'
		}))
	country = CountryField(blank_label='(select country)').formfield(attrs={
		'class': "custom-select",
		})
	state = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':"Tehran",
		'class': 'form-control'
		}))
	city = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':"Tehran",
		'class': 'form-control'
		}))
	zip_code = forms.CharField(widget=forms.TextInput(attrs={
		'placeholder':"1234",
		'class': 'form-control'
		}))
	create_account = forms.BooleanField(widget=forms.CheckboxInput())
	different_billing_address = forms.BooleanField(widget=forms.CheckboxInput())
	payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)