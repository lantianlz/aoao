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
    20102: u'洗车行名称重复',
    20103: u'洗车行不存在或者已删除',
    20104: u'该洗车行已添加此服务类型',
}
dict_err.update(consts.G_DICT_ERROR)


def car_wash_required(func):
    def _decorator(self, car_wash, *args, **kwargs):
        car_wash = car_wash
        if not isinstance(car_wash, CarWash):
            try:
                car_wash = CarWashBase().get_car_wash_by_id(car_wash)
            except CarWash.DoesNotExist:
                return 20103, dict_err.get(20103)
        return func(self, car_wash, *args, **kwargs)
    return _decorator


def service_type_required(func):
    def _decorator(self, service_type, *args, **kwargs):
        service_type = service_type
        if not isinstance(service_type, ServiceType):
            try:
                service_type = ServiceTypeBase().get_service_type_by_id(service_type)
            except ServiceType.DoesNotExist:
                return 20101, dict_err.get(20101)
        return func(self, service_type, *args, **kwargs)
    return _decorator


class CarWashBase(object):

    def get_car_wash_by_id(self, id, state=True):
        try:
            ps = dict(id=id)
            if state is not None:
                ps.update(state=state)
            return CarWash.objects.get(**ps)
        except CarWash.DoesNotExist:
            return ""

    def validate_car_wash_info(city_id, district_id, name, business_hours, tel, addr, lowest_sale_price, lowest_origin_price):
        assert all((city_id, district_id, name, business_hours, tel, addr))
        lowest_sale_price = float(lowest_sale_price)
        lowest_origin_price = float(lowest_origin_price)
        assert lowest_sale_price >= 0 and lowest_origin_price >= 0
        assert lowest_sale_price <= lowest_origin_price

    def add_car_wash(self, city_id, district_id, name, business_hours, tel, addr,
                     lowest_sale_price, lowest_origin_price, longitude, latitude, imgs, wash_type=0, des=None, note=None, sort_num=0):
        try:
            self.validate_car_wash_info(district_id, name, business_hours, tel, addr, lowest_sale_price, lowest_origin_price)
        except:
            return 99800, dict_err.get(99800)
        if CarWash.objects.filter(name=name):
            return 20102, dict_err.get(20102)

        ps = dict(city_id=city_id, district_id=district_id, name=name, business_hours=business_hours, tel=tel, addr=addr, des=des,
                  lowest_sale_price=lowest_sale_price, lowest_origin_price=lowest_origin_price, longitude=longitude, latitude=latitude, imgs=imgs,
                  wash_type=wash_type, note=note, sort_num=sort_num)
        car_wash = CarWash.objects.create(**ps)
        return 0, car_wash

    def get_car_washs_by_city_id(self, city_id, order_by="id"):
        return CarWash.objects.filter(city_id=city_id, state=True).order_by(order_by)


class ServicePriceBase(object):

    @car_wash_required
    def add_service_price(self, car_wash, service_type_id, sale_price, origin_price, clear_price, sort_num=0):
        try:
            sale_price = float(sale_price)
            origin_price = float(origin_price)
            clear_price = float(clear_price)
            assert sale_price < origin_price
        except:
            return 99800, dict_err.get(99800)

        service_type = ServiceTypeBase().get_service_type_by_id(service_type_id)
        if not service_type:
            return 20101, dict_err.get(20101)
        if ServicePrice.objects.filter(car_wash=car_wash, service_type=service_type):
            return 20104, dict_err.get(20104)

        ps = dict(car_wash=car_wash, service_type=service_type, sale_price=sale_price,
                  origin_price=origin_price, clear_price=clear_price, sort_num=sort_num)
        sp = ServicePrice.objects.create(**ps)

        return 0, sp


class ServiceTypeBase(object):

    def get_service_type_by_id(self, id, state=True):
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
