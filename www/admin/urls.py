# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.admin.views',
                       url(r'^$', 'home'),
                       )

# 用户
urlpatterns += patterns('www.admin.views_user',

                        url(r'^user/modify_user$', 'modify_user'),
                        url(r'^user/get_user_by_id$', 'get_user_by_id'),
                        url(r'^user/search$', 'search'),
                        url(r'^user$', 'user'),
                        )

# 权限
urlpatterns += patterns('www.admin.views_permission',

                        url(r'^permission/cancel_admin$', 'cancel_admin'),
                        url(r'^permission/save_user_permission$', 'save_user_permission'),
                        url(r'^permission/get_user_permissions$', 'get_user_permissions'),
                        url(r'^permission/get_all_administrators$', 'get_all_administrators'),
                        url(r'^permission$', 'permission'),
                        )

# 洗车行
urlpatterns += patterns('www.admin.views_car_wash',
                        url(r'^car_wash/add_car_wash$', 'add_car_wash'),
                        url(r'^car_wash/modify_car_wash$', 'modify_car_wash'),
                        url(r'^car_wash/get_car_wash_by_id$', 'get_car_wash_by_id'),
                        url(r'^car_wash/search$', 'search'),
                        url(r'^car_wash$', 'car_wash'),
                        )

# 城市
urlpatterns += patterns('www.admin.views_city',

                        url(r'^city/city/get_citys_by_name$', 'get_citys_by_name'),
                        url(r'^city/city/get_districts_by_city$', 'get_districts_by_city'),
                        url(r'^city/city/modify_note$', 'modify_note'),
                        url(r'^city/city/modify_city$', 'modify_city'),
                        url(r'^city/city/get_city_by_id$', 'get_city_by_id'),
                        url(r'^city/city/search$', 'search'),
                        url(r'^city/city$', 'city'),
                        )

# 区
urlpatterns += patterns('www.admin.views_district',

                        url(r'^city/district/modify_district$', 'modify_district'),
                        url(r'^city/district/get_district_by_id$', 'get_district_by_id'),
                        url(r'^city/district/search$', 'search'),
                        url(r'^city/district$', 'district'),
                        )