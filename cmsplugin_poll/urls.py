from cmsplugin_poll import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<poll_id>\d+)/$', views.detail),
    url(r'^(?P<poll_id>\d+)/results/$', views.results),
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote),
]
