from django.shortcuts import render
from Profile.models import Profile
from .models import Appointment
from Application.models import Application
from Profile.forms import ProgressForm
from django.shortcuts import render, redirect
from django.db.models import Q
from Profile.forms import ProgressForm


def booking(request):
    if not request.user.is_authenticated():
        return render(request, 'Profile/login.html')
    else:
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
                          {'form': form, 'profile': profile, 'approved_app': approved_app, })
        elif profile.user_type == 'Student':
            try:
                application = Application.objects.get(app_student=request.user.id)
            except Application.DoesNotExist:
                application = None
                approved_app = Appointment.objects.filter(Q(stuID=profile.user) | Q(status="Pending"))

        if profile.user_type == 'Supervisor':
            all_appointments = Appointment.objects.filter(lecID=request.user)
        else:
            all_appointments = Appointment.objects.filter(stuID=request.user)
        return render(request, 'Appointment/bookings.html', {'all_appointments': all_appointments, 'profile': profile})
