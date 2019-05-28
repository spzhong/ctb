# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from .application import user
from .application import task
from .application import check
from .application import stream
from .application import other


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ctb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ctb/user/([a-z,A-Z]+)$', user.index),
    url(r'^ctb/task/([a-z,A-Z]+)$', task.index),
    url(r'^ctb/check/([a-z,A-Z]+)$', check.index),
    url(r'^ctb/stream/([a-z,A-Z]+)$', stream.index),
    url(r'^ctb/other/([a-z,A-Z]+)$', other.index),
)



