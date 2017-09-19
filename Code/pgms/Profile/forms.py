from django import forms
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import BaseProfile, Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label='First Name')
    last_name = forms.CharField(required=False, label='Last Name')
    # user_photo = forms.FileField(required=False, label='User Photo')

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'Save'))
        self.fields['first_name'] =  forms.CharField(initial=self.instance.user.first_name)
        self.fields['last_name'] =  forms.CharField(initial=self.instance.user.last_name)
        # self.fields['user_photo'] = forms.FileField(initial=self.instance.user_photo)

    class Meta:
        model = BaseProfile
        fields = ['user_photo', 'first_name', 'last_name', 'user_address']

    def save_all_fields_from_request(self, request):
        user, created = User.objects.get_or_create(id=request.user.id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        self.instance.user_photo = request.FILES['user_photo']
        self.save()