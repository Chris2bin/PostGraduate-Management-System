from django.conf.urls import url 
from . import views


app_name = 'Application'

urlpatterns = [
    url(r'^list/(?P<application_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^list/(?P<application_id>[0-9]+)/delete_application/$', views.delete_application, name='delete_application'),
    url(r'^list/$', views.list, name='list'),

    
]
