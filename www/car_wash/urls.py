# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('www.car_wash.views',
                       url(r'^$', 'index'),
                       url(r'^(?P<car_wash_id>\d+)$', 'car_wash_detail'),
                       url(r'^coupon$', 'my_coupons'),
                       url(r'^location$', 'location'),

                       url(r'^create_order/(?P<service_price_id>\d+)$', 'show_create_order'),
                       url(r'^order$', 'order'),
                       url(r'^order/(?P<order_detail_id>\w+)$', 'order_detail'),
                       url(r'^get_car_washs$', 'get_car_washs'),

                       url(r'^bind_mobile$', 'bind_mobile'),
                       url(r'^setting$', 'setting'),
                       )
