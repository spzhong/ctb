# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from .application import user
from .application import task


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ctb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ctb/user/([a-z,A-Z]+)$', user.index),
    url(r'^ctb/task/([a-z,A-Z]+)$', task.index),
)



