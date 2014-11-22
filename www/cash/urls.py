# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('www.cash.views',
                       url(r'^$', 'cash_index'),
                       url(r'^user_cash_record$', 'user_cash_record'),
                       url(r'^recharge$', 'recharge'),
                       )
