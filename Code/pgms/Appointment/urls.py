from django.conf.urls import url
from . import views


app_name = 'Appointment'

urlpatterns = [
    url(r'^Appointment/$', views.booking, name='booking'),
]
