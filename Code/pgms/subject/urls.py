from django.conf.urls import url
from . import views
from django.core.urlresolvers import reverse

app_name = 'subject'

urlpatterns = [
    #url(r'^$',views.home, name='home'),
    url(r'^subject/$',views.subject, name='subject'),
    url(r'^subject/enroll/$', views.enroll_subject, name='enroll'),
    url(r'^subject/delete/(?P<enroll_id>[0-9]+)/$', views.delete, name='delete'),
    ]