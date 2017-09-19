from django.conf.urls import url 
from . import views


app_name = 'Application'

urlpatterns = [
    url(r'^list/(?P<apply_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^list/(?P<apply_id>[0-9]+)/delete_apply/$', views.delete_apply, name='delete_apply'),
    url(r'^list/$', views.list, name='list'),
    url(r'^apply/$', views.ApplyRequire, name='ApplyRequire'),
    
]