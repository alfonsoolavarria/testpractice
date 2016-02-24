__author__="alfonso"
__date__ ="$22-feb-2016 $"

from django.conf.urls import url
from views import TestView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = (
    url(r'^$', csrf_exempt(TestView.as_view()), name='member'),
    url(r'^(?P<id>[0-9]+)/$', csrf_exempt(TestView.as_view()), name='member'),

)
