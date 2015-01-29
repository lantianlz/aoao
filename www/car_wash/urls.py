# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('www.car_wash.views',
                       url(r'^$', 'index'),
                       url(r'^map$', 'map', {'template_name': 'mobile/car_wash/map.html'}),
                       url(r'^(?P<car_wash_id>\d+)$', 'car_wash_detail', {'template_name': 'mobile/car_wash/car_wash_detail.html'}),
                       url(r'^coupon$', 'my_coupons', {'template_name': 'mobile/car_wash/coupon.html'}),
                       url(r'^location$', 'location'),
                       url(r'^show_create_order/(?P<service_price_id>\d+)$', 'show_create_order', {'template_name': 'mobile/car_wash/show_create_order.html'}),
                       url(r'^create_order/(?P<service_price_id>\d+)$', 'create_order'),
                       url(r'^order_code$', 'order_code', {'template_name': 'mobile/car_wash/order_code_list.html'}),
                       url(r'^order/(?P<trade_id>\w+)$', 'order_detail', {'template_name': 'mobile/car_wash/order_detail.html'}),
                       url(r'^weixinpay$', 'weixinpay'),

                       url(r'^get_car_washs$', 'get_car_washs'),
                       url(r'^refund_order/(?P<trade_id>\w+)$', 'refund_order'),
                       )
