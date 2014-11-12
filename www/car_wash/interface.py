# -*- coding: utf-8 -*-

import time
import random
import requests
import json
import logging
from django.conf import settings

from common import cache, debug
from www.misc import consts

from www.car_wash.models import CarWash, ServicePrice, ServiceType

dict_err = {
    20100: u'服务类型名称重复',
    20101: u'服务类型不存在或者已删除',
}
dict_err.update(consts.G_DICT_ERROR)


class CarWashBase(object):

    def __init__(self):
        pass

    def __del__(self):
        pass


class ServicePriceBase(object):

    def __init__(self):
        pass

    def __del__(self):
        pass


class ServiceTypeBase(object):

    def get_service_type_by_id(self, id, state=None):
        try:
            ps = dict(id=id)
            if state is not None:
                ps.update(state=state)
            return ServiceType.objects.get(**ps)
        except ServiceType.DoesNotExist:
            return ""

    def add_service_type(self, name, sort_num=0):
        if not name:
            return 99800, dict_err.get(99800)
        if ServiceType.objects.filter(name=name):
            return 20100, dict_err.get(20100)

        st = ServiceType.objects.create(name=name, sort_num=sort_num)
        return 0, st

    def modify_service_type(self, service_type_id, name, sort_num=0):
        if not name:
            return 99800, dict_err.get(99800)

        st = self.get_service_type_by_id(service_type_id)
        if not st:
            return 20101, dict_err.get(20101)

        if st.name != name and ServiceType.objects.filter(name=name):
            return 20100, dict_err.get(20100)

        st.name = name
        st.sort_num = sort_num
        st.save()
        return 0, st
