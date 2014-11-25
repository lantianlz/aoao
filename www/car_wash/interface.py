# -*- coding: utf-8 -*-

import datetime

from common import utils
from www.misc import consts

from www.account.interface import UserBase
from www.car_wash.models import CarWash, ServicePrice, ServiceType, Coupon

dict_err = {
    20100: u'服务类型名称重复',
    20101: u'服务类型不存在或者已删除',
    20102: u'洗车行名称重复',
    20103: u'洗车行不存在或者已删除',
    20104: u'该洗车行已添加此服务类型',

    20205: u'小概率事件发生，优惠券编码重复，请重新添加',
}
dict_err.update(consts.G_DICT_ERROR)


def car_wash_required(func):
    def _decorator(self, car_wash, *args, **kwargs):
        car_wash = car_wash
        if not isinstance(car_wash, CarWash):
            car_wash = CarWashBase().get_car_wash_by_id(car_wash)
            if not car_wash:
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

    def format_car_washs_for_ajax(self, objs):
        datas = []
        for obj in objs:
            datas.append(dict(id=obj.id, url=obj.get_url(), name=obj.name, cover=obj.get_cover(),
                              district=obj.get_district().district, wash_type=obj.get_wash_type_display(),
                              lowest_sale_price=obj.lowest_sale_price, lowest_origin_price=obj.lowest_origin_price,
                              price_minus=obj.get_price_minus()
                              ))
        return datas

    def get_car_wash_by_id(self, id, state=True):
        try:
            ps = dict(id=id)
            if state is not None:
                ps.update(state=state)
            return CarWash.objects.get(**ps)
        except CarWash.DoesNotExist:
            return ""

    def validate_car_wash_info(city_id, district_id, name, business_hours, tel, addr, lowest_sale_price, lowest_origin_price, imgs):
        assert all((city_id, district_id, name, business_hours, tel, addr, imgs))
        lowest_sale_price = float(lowest_sale_price)
        lowest_origin_price = float(lowest_origin_price)
        assert lowest_sale_price >= 0 and lowest_origin_price >= 0
        assert lowest_sale_price <= lowest_origin_price

    def add_car_wash(self, city_id, district_id, name, business_hours, tel, addr,
                     lowest_sale_price, lowest_origin_price, longitude, latitude, imgs, wash_type=0, des=None, note=None, sort_num=0, state=True):
        try:
            self.validate_car_wash_info(district_id, name, business_hours, tel, addr, lowest_sale_price, lowest_origin_price, imgs)
        except:
            return 99801, dict_err.get(99801)
        if CarWash.objects.filter(name=name):
            return 20102, dict_err.get(20102)

        ps = dict(city_id=city_id, district_id=district_id, name=name, business_hours=business_hours, tel=tel, addr=addr, des=des,
                  lowest_sale_price=lowest_sale_price, lowest_origin_price=lowest_origin_price, longitude=longitude, latitude=latitude, imgs=imgs,
                  wash_type=wash_type, note=note, sort_num=sort_num)
        
        try:
            car_wash = CarWash.objects.create(**ps)
        except:
            return 99900, dict_err.get(99900)
        return 0, car_wash

    def get_car_washs_by_city_id(self, city_id, order_by_value="0"):
        dict_order_by = {"0": "id", "1": "lowest_sale_price", "2": "-order_count"}
        order_by_field = dict_order_by.get(order_by_value)
        return CarWash.objects.filter(city_id=city_id, state=True).order_by(order_by_field)

    def search_car_washs_for_admin(self, name="", state=True):
        return CarWash.objects.filter(name__contains=name, state=state)

    def modify_car_wash(self, car_wash_id, city_id, district_id, name, business_hours, tel, addr,
                        lowest_sale_price, lowest_origin_price, longitude, latitude, imgs, wash_type=0, des=None, note=None, sort_num=0, state=True):
        if not car_wash_id:
            return 99800, dict_err.get(99800)

        obj = self.get_car_wash_by_id(car_wash_id, None)
        if not obj:
            return 20103, dict_err.get(20103)

        try:
            self.validate_car_wash_info(district_id, name, business_hours, tel, addr, lowest_sale_price, lowest_origin_price)
        except:
            return 99801, dict_err.get(99801)

        temp = CarWash.objects.filter(name=name)
        if temp and temp[0].id != obj.id:
            return 20102, dict_err.get(20102)

        ps = dict(city_id=city_id, district_id=district_id, name=name, business_hours=business_hours, tel=tel, addr=addr, des=des,
                  lowest_sale_price=lowest_sale_price, lowest_origin_price=lowest_origin_price, longitude=longitude, latitude=latitude, imgs=imgs,
                  wash_type=wash_type, note=note, sort_num=sort_num, state=state)

        for k, v in ps.items():
            setattr(obj, k, v)

        try:
            obj.save()
        except:
            return 99900, dict_err.get(99900)
            
        return 0, dict_err.get(0)


class ServicePriceBase(object):

    @car_wash_required
    def add_service_price(self, car_wash, service_type_id, sale_price, origin_price, clear_price, sort_num=0):
        try:
            sale_price = float(sale_price)
            origin_price = float(origin_price)
            clear_price = float(clear_price)
            assert sale_price <= origin_price
        except:
            return 99801, dict_err.get(99801)

        service_type = ServiceTypeBase().get_service_type_by_id(service_type_id)
        if not service_type:
            return 20101, dict_err.get(20101)
        if ServicePrice.objects.filter(car_wash=car_wash, service_type=service_type):
            return 20104, dict_err.get(20104)

        ps = dict(car_wash=car_wash, service_type=service_type, sale_price=sale_price,
                  origin_price=origin_price, clear_price=clear_price, sort_num=sort_num)
        sp = ServicePrice.objects.create(**ps)

        return 0, sp

    def get_service_prices_by_car_wash(self, car_wash, state=None):
        ps = dict(car_wash=car_wash)
        if state is not None:
            ps.update(state=state)
        return ServicePrice.objects.select_related("service_type").filter(**ps)


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

    def modify_service_type(self, service_type_id, name, sort_num=0, state=True):
        if not name:
            return 99800, dict_err.get(99800)

        st = self.get_service_type_by_id(service_type_id, state=None)
        if not st:
            return 20101, dict_err.get(20101)

        if st.name != name and ServiceType.objects.filter(name=name):
            return 20100, dict_err.get(20100)

        st.name = name
        st.sort_num = sort_num
        st.state = state
        st.save()
        return 0, st

    def search_types_for_admin(self):
        return ServiceType.objects.all()


class CouponBase(object):

    def add_coupon(self, coupon_type, discount, expiry_time, user_id=None, minimum_amount=0, car_wash_id=None):
        try:
            discount = float(discount)
            minimum_amount = float(minimum_amount)

            assert discount >= 0 and minimum_amount >= 0 and expiry_time > datetime.datetime.now()
            if minimum_amount > 0:
                assert minimum_amount > discount
        except:
            return 99801, dict_err.get(99801)

        if user_id and not UserBase().get_user_login_by_id(user_id):
            return 99600, dict_err.get(99600)

        car_wash = None
        if car_wash_id:
            car_wash = CarWashBase().get_car_wash_by_id(car_wash_id)
            if not car_wash:
                return 20103, dict_err.get(20103)

        code = utils.get_radmon_int(length=12)
        if Coupon.objects.filter(code=code):
            return 20205, dict_err.get(20205)

        ps = dict(code=code, coupon_type=coupon_type, discount=discount, expiry_time=expiry_time,
                  user_id=user_id, minimum_amount=minimum_amount, car_wash=car_wash)
        coupon = Coupon.objects.create(**ps)

        return 0, coupon

    def get_coupons_by_user_id(self, user_id):
        return Coupon.objects.filter(user_id=user_id)
