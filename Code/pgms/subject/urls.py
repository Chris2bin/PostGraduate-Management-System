from django.conf.urls import url
from . import views
from django.core.urlresolvers import reverse

app_name = 'subject'

urlpatterns = [
    #url(r'^$',views.home, name='home'),
    url(r'^$',views.home, name='home'),
    url(r'^enroll/$', views.enroll_subject, name='enroll'),
    url(r'^delete/(?P<enroll_id>[0-9]+)/$', views.delete, name='delete'),
    ]