from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'file'

urlpatterns = [
    #url('^file/',include('file.urls'),namespace='file'),
    url(r'^$', views.home, name='file'),
    url(r'^uploads/$', views.upload, name='upload'),
    url(r'^delete/(?P<file_id>[0-9]+)/$', views.delete_file, name='delete'),
]

