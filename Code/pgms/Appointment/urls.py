from django.conf.urls import url
from . import views

app_name = 'Appointment'

urlpatterns = [
    url(r'^Appointment/$', views.booking, name='booking'),
    url(r'^make_appointment/$', views.make_appointment, name='make_appointment'),
]
