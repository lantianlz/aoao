# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
                       url(r'^login$', 'www.account.views.login'),
                       url(r'^logout$', 'www.account.views.logout'),
                       url(r'^regist$', 'www.account.views.regist'),
                       url(r'^forget_password$', 'www.account.views.forget_password'),
                       url(r'^qiniu_img_return$', 'www.misc.views.qiniu_img_return'),
                       url(r'^save_img$', 'www.misc.views.save_img'),
                       url(r'^crop_img$', 'www.misc.views.crop_img'),

                       url(r'^$', 'www.car_wash.views.index'),
                       url(r'^car_wash/', include('www.car_wash.urls')),
                       url(r'^account/', include('www.account.urls')),
                       url(r'^weixin/', include('www.weixin.urls')),
                       url(r'^city/', include('www.city.urls')),
                       url(r'^cash/', include('www.cash.urls')),

                       url(r'^admin/', include('www.admin.urls')),

                       url(r'^n/(?P<nick>.*)$', 'www.account.views.get_user_by_nick'),
                       url(r'^p/(?P<user_id>\w+)?$', 'www.account.views.user_journey'),
                       url(r'^p/(?P<user_id>\w+)/user_answer$', 'www.account.views.user_answer'),


                       url(r'^(?P<txt_file_name>\w+)\.txt$', 'www.misc.views.txt_view'),
                       url(r'^s/(?P<template_name>.*)$', 'www.misc.views.static_view'),
                       url(r'^500$', 'www.misc.views.test500'),
                       url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': False}),

                       url(r'^crossdomain.xml$', direct_to_template, {'template': 'crossdomain.xml'}),
                       )

urlpatterns += patterns('misc.views_paycallback',
                        (r'^alipaycallback_m$', 'alipaycallback_m'),
                        (r'^alipaynotify_m$', 'alipaynotify_m'),
                        (r'^weixinpaycallback$', 'weixinpaycallback'),

                        (r'^test_paycallback$', 'test_paycallback'),
                        )
