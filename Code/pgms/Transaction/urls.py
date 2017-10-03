from django.conf.urls import url
from . import views

app_name = 'Transaction'

urlpatterns = [
    url(r'^transaction/$', views.account, name='account'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
]