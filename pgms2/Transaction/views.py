from django.shortcuts import render
from django.template import loader
from .models import Transaction


def account(request):
    all_account = Transaction.objects.all()
    context = {
        'all_account': all_account,
    }
    return render(request, 'Transaction/account.html', context)
