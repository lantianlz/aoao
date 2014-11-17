# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('www.car_wash.views',
                       url(r'^$', 'index'),
                       url(r'^(?P<car_wash_id>\d+)$', 'detail'),
                       url(r'^order$', 'order'),
                       url(r'^order/(?P<order_detail_id>\d+)$', 'order_detail'),
					   url(r'^coupon$', 'coupon'),
					   url(r'^account$', 'account'),
					   url(r'^record_deal$', 'record_deal'),
					   url(r'^bind_mobile$', 'bind_mobile'),
					   url(r'^about$', 'about'),
					   url(r'^setting$', 'setting'),
					   url(r'^pay$', 'pay'),
					   url(r'^buy$', 'buy'),
					   url(r'^unopen_city$', 'unopen_city'),
					   url(r'^location$', 'location'),
                       )
