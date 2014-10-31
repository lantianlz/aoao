# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('www.car_wash.views',
                       url(r'^$', 'index'),
                       url(r'^(?P<car_wash_id>\d+)$', 'detail'),


                       url(r'^citys$', 'show_open_citys'),
                       url(r'^provinces$', 'provinces_list'),
                       url(r'^province/(?P<province_id>\d+)$', 'cities_list')
                       )
