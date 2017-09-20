from django import forms

from .models import Subject,Enroll


class EnrollForm(forms.ModelForm):
    class Meta:
        model = Enroll
        fields = ('student','subject')
        widgets = {'student': forms.HiddenInput()}

