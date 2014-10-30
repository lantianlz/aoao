# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'www.car_wash.views.index'),
    url(r'^(?P<car_wash_id>\d+)$', 'www.car_wash.views.detail')
)