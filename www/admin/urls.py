# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.admin.views',
                       url(r'^$', 'home'),
                       )

# 用户
urlpatterns += patterns('www.admin.views_user',

                        url(r'^user/get_user_by_nick$', 'get_user_by_nick'),
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
                        url(r'^car_wash/car_wash/get_car_washs_by_name$', 'get_car_washs_by_name'),
                        url(r'^car_wash/car_wash/add_car_wash$', 'add_car_wash'),
                        url(r'^car_wash/car_wash/modify_car_wash$', 'modify_car_wash'),
                        url(r'^car_wash/car_wash/get_car_wash_by_id$', 'get_car_wash_by_id'),
                        url(r'^car_wash/car_wash/search$', 'search'),
                        url(r'^car_wash/car_wash$', 'car_wash'),
                        )

# 洗车行服务类型
urlpatterns += patterns('www.admin.views_service_type',
                        url(r'^car_wash/service_type/add_service_type$', 'add_service_type'),
                        url(r'^car_wash/service_type/modify_service_type$', 'modify_service_type'),
                        url(r'^car_wash/service_type/get_service_type_by_id$', 'get_service_type_by_id'),
                        url(r'^car_wash/service_type/search$', 'search'),
                        url(r'^car_wash/service_type$', 'service_type'),
                        )

# 洗车行服务价格
urlpatterns += patterns('www.admin.views_service_price',
                        url(r'^car_wash/service_price/add_service_price$', 'add_service_price'),
                        url(r'^car_wash/service_price/modify_service_price$', 'modify_service_price'),
                        url(r'^car_wash/service_price/get_service_price_by_id$', 'get_service_price_by_id'),
                        url(r'^car_wash/service_price/search$', 'search'),
                        url(r'^car_wash/service_price$', 'service_price'),
                        )

# 洗车行银行信息
urlpatterns += patterns('www.admin.views_bank',
                        url(r'^car_wash/bank/add_bank$', 'add_bank'),
                        url(r'^car_wash/bank/modify_bank$', 'modify_bank'),
                        url(r'^car_wash/bank/get_bank_by_id$', 'get_bank_by_id'),
                        url(r'^car_wash/bank/search$', 'search'),
                        url(r'^car_wash/bank$', 'bank'),
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

# 统计
urlpatterns += patterns('www.admin.views_statistics',

                        url(r'^statistics/get_active_user$', 'get_active_user'),
                        url(r'^statistics/active_user$', 'active_user'),
                        )

# 常用工具
urlpatterns += patterns('www.admin.views_caches',

                        # 缓存管理
                        url(r'^tools/caches/get_cache$', 'get_cache'),
                        url(r'^tools/caches/remove_cache$', 'remove_cache'),
                        url(r'^tools/caches/modify_cache$', 'modify_cache'),
                        url(r'^tools/caches$', 'caches'),
                        )

# 优惠券
urlpatterns += patterns('www.admin.views_coupon',

                        url(r'^coupon/search$', 'search'),
                        url(r'^coupon/add_coupon$', 'add_coupon'),
                        url(r'^coupon$', 'coupon'),
                        )