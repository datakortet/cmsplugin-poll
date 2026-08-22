from django.urls import include, path


urlpatterns = [
    path('poll/', include('cmsplugin_poll.urls')),
]
