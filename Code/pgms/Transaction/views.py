from django.shortcuts import render
from django.template import loader
from .models import Transaction
from .forms import TransactionForm
from Profile.models import Profile
from Appointment.models import Appointment
from Application.models import Application
from django.db.models import Q
from Profile.forms import ProgressForm


def account(request):
    profile = Profile.objects.get(pk=request.user.id)

    # Search bar stuff
    all_profiles = Profile.objects.all().filter(
        Q(user_type="Supervisor") | Q(user_type="Student")
    ).distinct()
    query = request.GET.get("q")
    if query:
        all_profiles = all_profiles.filter(
            Q(user__username__contains=query) | Q(user_type__contains=query) | Q(
                user__first_name__contains=query) | Q(user__last_name__contains=query)
        ).distinct()
        return render(request, 'Profile/search.html',
                      {'all_profiles': all_profiles, 'profile': profile, 'application': application, })

    # Notification bar stuff
    if profile.user_type == 'Supervisor':
        approved_app = Appointment.objects.filter(lecID=profile.user)
        form = ProgressForm(request.POST or None)
        if request.POST:
            if form.is_valid():
                progress = form.cleaned_data.get("br_progress")
                target_profile.br_progress = progress
                target_profile.save()
        if request.POST.get("reject"):
            appointmentID = request.POST.get('appointment_id', False)
            app = Appointment.objects.get(pk=appointmentID)
            app.status = "Reject"
            app.save()
        elif request.POST.get("accept"):
            appointmentID = request.POST.get('appointment_id', False)
            app = Appointment.objects.get(pk=appointmentID)
            app.status = "Approve"
            app.save()

            return render(request, 'Transaction/account.html', {'all_account': all_account, 'profile': profile})
    elif profile.user_type == 'Student':
        try:
            application = Application.objects.get(app_student=request.user.id)
        except Application.DoesNotExist:
            application = None
            approved_app = Appointment.objects.filter(Q(stuID=profile.user) | Q(status="Pending"))

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

    # Search bar stuff
    all_profiles = Profile.objects.all().filter(
        Q(user_type="Supervisor") | Q(user_type="Student")
    ).distinct()
    query = request.GET.get("q")
    if query:
        all_profiles = all_profiles.filter(
            Q(user__username__contains=query) | Q(user_type__contains=query) | Q(
                user__first_name__contains=query) | Q(user__last_name__contains=query)
        ).distinct()
        return render(request, 'Profile/search.html',
                      {'all_profiles': all_profiles, 'profile': profile, 'application': application, })

    # Notification bar stuff
    if profile.user_type == 'Supervisor':
        approved_app = Appointment.objects.filter(lecID=profile.user)
        form = ProgressForm(request.POST or None)
        if request.POST:
            if form.is_valid():
                progress = form.cleaned_data.get("br_progress")
                target_profile.br_progress = progress
                target_profile.save()
        if request.POST.get("reject"):
            appointmentID = request.POST.get('appointment_id', False)
            app = Appointment.objects.get(pk=appointmentID)
            app.status = "Reject"
            app.save()
        elif request.POST.get("accept"):
            appointmentID = request.POST.get('appointment_id', False)
            app = Appointment.objects.get(pk=appointmentID)
            app.status = "Approve"
            app.save()

        return render(request, 'Transaction/account.html', {'all_account': all_account, 'profile': profile})
    elif profile.user_type == 'Student':
        try:
            application = Application.objects.get(app_student=request.user.id)
        except Application.DoesNotExist:
            application = None
            approved_app = Appointment.objects.filter(Q(stuID=profile.user) | Q(status="Pending"))

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
