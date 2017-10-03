from django.shortcuts import render
from django.template import loader
from .models import Transaction
from .forms import TransactionForm
from Profile.models import Profile


def account(request):
    profile = Profile.objects.get(pk=request.user.id)
    all_account = Transaction.objects.filter(StuID=request.user)
    fees_paid = 0
    for transaction in all_account:
        if transaction.Tran_Pend == "Approve" and transaction.Tran_calc == False:
            fees_paid += transaction.Tran_Paid
            transaction.Tran_calc = True
            transaction.save()
    profile.user_feesOwed -= fees_paid
    profile.save()
    return render(request, 'Transaction/account.html', {'all_account': all_account, 'profile': profile})

def upload_file(request):
    profile = Profile.objects.get(pk=request.user.id)
    all_account = Transaction.objects.filter(StuID=request.user)
    if not request.user.is_authenticated():
        return render(request, 'Profile/login.html')
    else:
        if request.POST.get("transaction") == "Transaction":
            if request.POST:
                form = TransactionForm(request.POST, request.FILES)
                if form.is_valid():
                    transaction = form.save(commit=False)
                    transaction.StuID = request.user
                    transaction.Tran_Pend = "Pending"
                    transaction.save()
                return render(request, 'Transaction/account.html', {'all_account': all_account, 'profile': profile})
    return render(request, 'Transaction/upload_file.html', {'all_account': all_account, 'profile': profile})
