from django.conf.urls import url
from . import views

app_name = 'Transaction'

urlpatterns = [
    url(r'^$', views.account, name='account'),
]
from django.conf.urls import url
from . import views

app_name = 'Transaction'

urlpatterns = [
    url(r'^$', views.account, name='account'),
]