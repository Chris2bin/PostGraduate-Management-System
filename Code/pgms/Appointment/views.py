from django.shortcuts import render
from Profile.models import Profile
from .models import Appointment
from django.shortcuts import render, redirect


def booking(request):
    if not request.user.is_authenticated():
        return render(request, 'Profile/login.html')
    else:
        profile = Profile.objects.get(pk=request.user.id)
        if profile.user_type == 'Supervisor':
            all_appointments = Appointment.objects.filter(lecID=request.user)
        else:
            all_appointments = Appointment.objects.filter(stuID=request.user)
        return render(request, 'Appointment/bookings.html', {'all_appointments': all_appointments, 'profile': profile})
