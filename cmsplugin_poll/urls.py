from cmsplugin_poll import views
from django.urls import re_path as url


app_name = 'cmsplugin_poll'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='poll_detail'),
    url(r'^(?P<poll_id>\d+)/results/$', views.results, name="results"),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name="vote"),
]
