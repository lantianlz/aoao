# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('www.cash.views',
                       url(r'^$', 'cash_index'),
                       url(r'^user_cash_record$', 'user_cash_record', {'template_name': 'mobile/cash/user_cash_record.html'}),
                       url(r'^recharge$', 'recharge', {'template_name': 'mobile/cash/recharge.html'}),
                       url(r'^bind_mobile$', 'bind_mobile'),
                       url(r'^setting$', 'setting'),
                       )
