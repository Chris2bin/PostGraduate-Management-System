from django.contrib.auth.models import User
from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['app_name_first','app_name_last','app_birthday','app_gender','app_address','app_email','app_ic','app_nation','app_mobile_number','app_file_upload','app_file_upload2','app_file_upload3','app_type','app_programme']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password','email', 'first_name', 'last_name']