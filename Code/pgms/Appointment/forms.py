from django import forms
from django.contrib.auth.models import User
from .models import Appointment


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'reason', 'lecID', 'stuID']

    def save_all_fields_from_request(self, request):
        self.save()
        Appointment.date = request.POST['date']
        Appointment.time = request.POST['time']
        Appointment.reason = request.POST['reason']
        Appointment.lecID = request.POST['lecID']
        Appointment.stuID = request.POST['stuID']
        Appointment.save()