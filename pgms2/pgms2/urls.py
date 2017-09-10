from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^Appointment/', include('Appointment.urls')),
    url(r'^Transaction/', include('Transaction.urls')),
]
