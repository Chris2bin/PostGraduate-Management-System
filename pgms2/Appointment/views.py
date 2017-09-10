from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Appointment
from .forms import AppointmentForm


def booking(request):
    all_appointments = Appointment.objects.all()
    context = {
        'all_appointments': all_appointments,
    }
    return render(request, 'Appointment/bookings.html', context)


def make_appointment(request):
    form = AppointmentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        appointment = form.save(commit=False)
        appointment.date = form.cleaned_data.get("date")
        appointment.time = form.cleaned_data.get("time")
        appointment.stuID = form.cleaned_data.get("stuID")
        appointment.lecID = form.cleaned_data.get("lecID")
        appointment.save()
        all_appointments = Appointment.objects.all()
        context = {
            'all_appointments': all_appointments,
        }
        return render(request, 'Appointment/bookings.html', context)
    context = {
        "form": form,
    }
    return render(request, 'Appointment/form.html', context)