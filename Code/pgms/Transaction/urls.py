from django.conf.urls import url
from . import views

app_name = 'Transaction'

urlpatterns = [
    url(r'^Transaction/$', views.account, name='account'),
]