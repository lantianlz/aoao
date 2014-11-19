# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('www.cash.views',

                       url(r'^$', 'cash_index'),
                       url(r'^record_deal$', 'record_deal'),
                       url(r'^pay$', 'pay'),

                       )
