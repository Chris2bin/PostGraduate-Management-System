from django.shortcuts import render, redirect,get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404
from Profile.models import Profile
from django.contrib.auth import logout
from .models import Subject, Enroll
from .forms import EnrollForm
from Appointment.models import Appointment
from Application.models import Application
from django.db.models import Q
from Profile.forms import ProgressForm

# Create your views here.

def subject(request):
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

            return render(request, 'subject/Subject.html', {'subjects': subjects, 'profile': profile, })
    elif profile.user_type == 'Student':
        try:
            application = Application.objects.get(app_student=request.user.id)
        except Application.DoesNotExist:
            application = None
            approved_app = Appointment.objects.filter(Q(stuID=profile.user) | Q(status="Pending"))

    if profile.user_type == 'Admin':
        logout(request)
        return render(request, 'Profile/login.html', {'error_message': 'You are NOT allowed to enter this page.'})
    else:
        subjects = Enroll.objects.filter(student=request.user)
        return render(request, 'subject/Subject.html',{'subjects': subjects, 'profile': profile, })

def delete(request, enroll_id):
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

        return render(request, 'Profile/profile_supervisor.html',
                      {'form': form, 'profile': profile, 'target_profile': target_profile,
                       'approved_app': approved_app, })
    elif profile.user_type == 'Student':
        try:
            application = Application.objects.get(app_student=request.user.id)
        except Application.DoesNotExist:
            application = None
            approved_app = Appointment.objects.filter(Q(stuID=profile.user) | Q(status="Pending"))

    if profile.user_type == 'Admin':
        logout(request)
        return render(request, 'Profile/login.html', {'error_message': 'You are NOT allowed to enter this page.'})

    else:
        enroll = Enroll.objects.get(pk=enroll_id)
        fee = enroll.subject.fee
        profile.user_feesOwed -= fee
        profile.save()
        enroll.delete()
        return redirect('subject:subject')

def enroll_subject(request):
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

        return render(request, 'Profile/profile_supervisor.html',
                      {'form': form, 'profile': profile, 'target_profile': target_profile,
                       'approved_app': approved_app, })
    elif profile.user_type == 'Student':
        try:
            application = Application.objects.get(app_student=request.user.id)
        except Application.DoesNotExist:
            application = None
            approved_app = Appointment.objects.filter(Q(stuID=profile.user) | Q(status="Pending"))

    if profile.user_type == 'Admin':
        logout(request)
        return render(request, 'Profile/login.html', {'error_message': 'You are NOT allowed to enter this page.'})
    else:
        student = request.user
        form = EnrollForm(request.POST or None, initial={'student': student})
        form.fields["subject"].queryset = Subject.objects.exclude(enroll__student=student)
        if form.is_valid():
            enroll = form.save(commit=False)
            enroll.student = request.user
            fee = enroll.subject.fee
            profile.user_feesOwed += fee
            enroll.save()
            profile.save()
            return redirect('subject:subject')
        return render(request, 'subject/enroll.html', {'form': form, 'profile':profile})

