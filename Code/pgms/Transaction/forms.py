from django import forms
from django.contrib.auth.models import User
from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['Tran_File', 'Tran_RefNo']
