from django.conf.urls import url
from . import views

app_name = 'Profile'

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
]