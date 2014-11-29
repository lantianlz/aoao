# -*- coding: utf-8 -*-

'''
全局常量维护
'''

G_DICT_ERROR = {
    99600: u'不存在的用户',
    99700: u'权限不足',
    99800: u'参数缺失',
    99801: u'参数异常',
    99900: u'系统错误',
    0: u'成功'
}


PERMISSIONS = [
    {'code': 'permission_manage', 'name': u'权限管理', 'parent': None},
    {'code': 'add_user_permission', 'name': u'添加用户权限', 'parent': 'permission_manage'},
    {'code': 'query_user_permission', 'name': u'查询用户权限', 'parent': 'permission_manage'},
    {'code': 'modify_user_permission', 'name': u'修改用户权限', 'parent': 'permission_manage'},
    {'code': 'cancel_admin', 'name': u'取消管理员', 'parent': 'permission_manage'},

    {'code': 'user_manage', 'name': u'用户管理', 'parent': None},
    #{'code': 'add_user', 'name': u'添加用户', 'parent': 'user_manage'},
    {'code': 'query_user', 'name': u'查询用户', 'parent': 'user_manage'},
    {'code': 'modify_user', 'name': u'修改用户', 'parent': 'user_manage'},
    {'code': 'remove_user', 'name': u'删除用户', 'parent': 'user_manage'},

    {'code': 'city_manage', 'name': u'城市管理', 'parent': None},
    #{'code': 'add_city', 'name': u'添加城市', 'parent': 'city_manage'},
    {'code': 'query_city', 'name': u'查询城市', 'parent': 'city_manage'},
    {'code': 'modify_city', 'name': u'修改城市', 'parent': 'city_manage'},

    {'code': 'district_manage', 'name': u'区管理', 'parent': None},
    #{'code': 'add_district', 'name': u'添加区', 'parent': 'district_manage'},
    {'code': 'query_district', 'name': u'查询区', 'parent': 'district_manage'},
    {'code': 'modify_district', 'name': u'修改区', 'parent': 'district_manage'},

    {'code': 'car_wash_manage', 'name': u'洗车行管理', 'parent': None},
    {'code': 'add_car_wash', 'name': u'添加洗车行', 'parent': 'car_wash_manage'},
    {'code': 'query_car_wash', 'name': u'查询洗车行', 'parent': 'car_wash_manage'},
    {'code': 'modify_car_wash', 'name': u'修改洗车行', 'parent': 'car_wash_manage'},

    {'code': 'service_type_manage', 'name': u'服务类别管理', 'parent': None},
    {'code': 'add_service_type', 'name': u'添加服务类别', 'parent': 'service_type_manage'},
    {'code': 'query_service_type', 'name': u'查询服务类别', 'parent': 'service_type_manage'},
    {'code': 'modify_service_type', 'name': u'修改服务类别', 'parent': 'service_type_manage'},

    {'code': 'service_price_manage', 'name': u'服务价格管理', 'parent': None},
    {'code': 'add_service_price', 'name': u'添加服务价格', 'parent': 'service_price_manage'},
    {'code': 'query_service_price', 'name': u'查询服务价格', 'parent': 'service_price_manage'},
    {'code': 'modify_service_price', 'name': u'修改服务价格', 'parent': 'service_price_manage'},

    {'code': 'car_wash_bank_manage', 'name': u'洗车行银行信息管理', 'parent': None},
    {'code': 'add_car_wash_bank', 'name': u'添加洗车行银行信息', 'parent': 'car_wash_bank_manage'},
    {'code': 'query_car_wash_bank', 'name': u'查询洗车行银行信息', 'parent': 'car_wash_bank_manage'},
    {'code': 'modify_car_wash_bank', 'name': u'修改洗车行银行信息', 'parent': 'car_wash_bank_manage'},

    {'code': 'tools', 'name': u'常用工具', 'parent': None},
    {'code': 'get_cache', 'name': u'查询缓存', 'parent': 'tools'},
    {'code': 'remove_cache', 'name': u'删除缓存', 'parent': 'tools'},
    {'code': 'modify_cache', 'name': u'修改缓存', 'parent': 'tools'},

    {'code': 'statistics_manage', 'name': u'统计管理', 'parent': None},
    {'code': 'statistics_active_user', 'name': u'当日活跃用户统计', 'parent': 'statistics_manage'},
    
]
