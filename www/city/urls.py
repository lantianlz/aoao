# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('www.city.views',

                       url(r'^citys$', 'show_open_citys'),
                       url(r'^provinces$', 'provinces_list'),
                       url(r'^province/(?P<province_id>\d+)$', 'cities')
                       )
