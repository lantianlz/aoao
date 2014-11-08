# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('www.car_wash.views',
                       url(r'^$', 'index'),
                       url(r'^(?P<car_wash_id>\d+)$', 'detail'),
                       url(r'^order$', 'order'),
                       url(r'^order/(?P<order_detail_id>\d+)$', 'order_detail'),
					   url(r'^coupon$', 'coupon'),
                       )
