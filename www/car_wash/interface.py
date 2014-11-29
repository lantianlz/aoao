# -*- coding: utf-8 -*-

import datetime
import logging
from django.db import transaction

from common import utils, debug
from www.misc import consts

from www.account.interface import UserBase
from www.car_wash.models import CarWash, ServicePrice, ServiceType, Coupon, Order, OrderCode, CarWashBank

dict_err = {
    20100: u'服务类型名称重复',
    20101: u'服务类型不存在或者已删除',
    20102: u'洗车行名称重复',
    20103: u'洗车行不存在或者已删除',
    20104: u'该洗车行已添加此服务类型',
    20105: u'该服务价格不存在或者已删除',
    20106: u'该洗车行已添加此服务价格',
    20107: u'该洗车行银行信息已存在',
    20108: u'该洗车行银行信息不存在或者已删除',

    20201: u'优惠券不存在',
    20205: u'小概率事件发生，优惠券编码重复，请重新添加',
}
dict_err.update(consts.G_DICT_ERROR)

DEFAULT_DB = 'default'


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
            self.validate_car_wash_info(district_id, name, business_hours, tel, addr, lowest_sale_price, lowest_origin_price, imgs)
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

    def get_car_washs_by_name(self, name=""):
        objs = CarWash.objects.filter(state=True)

        if name:
            objs = objs.filter(name__contains=name)

        return objs[:10]

    def get_car_wash_by_name(self, name=""):
        objs = CarWash.objects.filter(state=True)

        if name:
            objs = objs.filter(name=name)

        return objs


class ServicePriceBase(object):

    @car_wash_required
    def add_service_price(self, car_wash_obj_or_id, service_type_id, sale_price, origin_price, clear_price, sort_num=0):
        try:
            sale_price = float(sale_price)
            origin_price = float(origin_price)
            clear_price = float(clear_price)
            assert sale_price <= origin_price
        except:
            return 99801, dict_err.get(99801)

        if not isinstance(car_wash_obj_or_id, CarWash):
            car_wash = self.get_car_wash_by_id(car_wash_obj_or_id)
        else:
            car_wash = car_wash_obj_or_id

        service_type = ServiceTypeBase().get_service_type_by_id(service_type_id)
        if not service_type:
            return 20101, dict_err.get(20101)
        if ServicePrice.objects.filter(car_wash=car_wash, service_type=service_type):
            return 20104, dict_err.get(20104)

        ps = dict(car_wash=car_wash, service_type=service_type, sale_price=sale_price,
                  origin_price=origin_price, clear_price=clear_price, sort_num=sort_num)
        sp = ServicePrice.objects.create(**ps)

        return 0, sp

    def get_service_prices_by_car_wash(self, car_wash, state=True):
        ps = dict(car_wash=car_wash)
        if state is not None:
            ps.update(state=state)
        return ServicePrice.objects.select_related("service_type").filter(**ps)

    def search_prices_for_admin(self, car_wash_name, state=True):
        objs = ServicePrice.objects.filter(state=state)

        if car_wash_name:
            car_wash = CarWashBase().get_car_wash_by_name(car_wash_name)

            objs = objs.filter(car_wash=car_wash)

        return objs

    def get_service_price_by_id(self, price_id, state=True):
        objs = ServicePrice.objects.select_related("car_wash", "service_type").filter(pk=price_id)
        if state != None:
            objs = objs.filter(state=state)

        return objs[0] if objs else None

    def modify_service_price(self, price_id, car_wash_id, service_type_id, sale_price, origin_price, clear_price, sort_num=0, state=True):
        try:
            sale_price = float(sale_price)
            origin_price = float(origin_price)
            clear_price = float(clear_price)
            assert sale_price <= origin_price
        except:
            return 99801, dict_err.get(99801)

        obj = self.get_service_price_by_id(price_id, None)
        if not obj:
            return 20105, dict_err.get(20105)

        car_wash = CarWashBase().get_car_wash_by_id(car_wash_id)
        if not car_wash:
            return 20103, dict_err.get(20103)

        service_type = ServiceTypeBase().get_service_type_by_id(service_type_id)
        if not service_type:
            return 20101, dict_err.get(20101)

        temp = ServicePrice.objects.filter(car_wash=car_wash, service_type=service_type)

        if temp and temp[0] != obj:
            return 20106, dict_err.get(20106)

        ps = dict(car_wash=car_wash, service_type=service_type, sale_price=sale_price,
                  origin_price=origin_price, clear_price=clear_price, sort_num=sort_num, state=state)

        for k, v in ps.items():
            setattr(obj, k, v)

        try:
            obj.save()
        except:
            return 99900, dict_err.get(99900)

        return 0, dict_err.get(0)


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

    def get_all_types(self, state=True):
        objs = ServiceType.objects.all()

        if state:
            objs.filter(state=state)

        return objs


# ===================================================订单和优惠券部分=================================================================#
class CouponBase(object):

    def get_coupon_by_id(self, id, user_id=None, state=1):
        try:
            ps = dict(id=id)
            if user_id is not None:
                ps.update(user_id=user_id)
            if state is not None:
                ps.update(state=state)
            return Coupon.objects.get(**ps)
        except Coupon.DoesNotExist:
            return ""

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

    def get_valid_coupon_by_user_id(self, user_id):
        coupons = Coupon.objects.filter(user_id=user_id, state=1)
        datas = []
        for coupon in coupons:
            if coupon.check_is_expiry():
                datas.append(coupon)
        return coupons


class OrderBase(object):

    def validate_order_info(self, service_type, user_id, count, pay_type):
        assert service_type and user_id and count and pay_type
        count = int(count)
        pay_type = int(pay_type)
        assert 1 <= count <= 5
        assert pay_type in (0, 1, 2)

    def valide_coupon(self, coupon, pay_fee):
        """
        @note: 检测优惠码是否可用
        """
        pass

    @transaction.commit_manually(using=DEFAULT_DB)
    def create_order(self, service_price_id_or_object, user_id, count, pay_type, coupon_id=None, use_user_cash=False):
        try:
            service_type = service_price_id_or_object if isinstance(service_price_id_or_object, ServicePrice) \
                else ServicePriceBase().get_service_price_by_id(service_price_id_or_object)

            try:
                self.validate_order_info(service_type, user_id, count, pay_type)
            except:
                return 99801, dict_err.get(99801)

            coupon = None
            if coupon_id:
                coupon = CouponBase().get_coupon_by_id(coupon_id, user_id)
                if not coupon:
                    transaction.rollback(using=DEFAULT_DB)
                    return 20201, dict_err.get(20201)

            transaction.commit(using=DEFAULT_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            logging.error(debug.get_debug_detail(e))
            transaction.rollback(using=DEFAULT_DB)
            return 99900, dict_err.get(99900)


class OrderCodeBase(object):
    pass


class CarWashBankBase(object):

    def get_bank_by_car_wash(self, car_wash_id):
        return CarWashBank.objects.filter(car_wash__id=car_wash_id)

    def add_bank(self, car_wash_id, manager_name, mobile, tel, bank_name, bank_card, balance_date):
        if not (car_wash_id and manager_name and mobile
                and tel and bank_name and bank_card and balance_date):
            return 99800, dict_err.get(99800)

        if self.get_bank_by_car_wash(car_wash_id):
            return 20107, dict_err.get(20107)

        ps = dict(
            car_wash_id=car_wash_id,
            manager_name=manager_name,
            mobile=mobile,
            tel=tel,
            bank_name=bank_name,
            bank_card=bank_card,
            balance_date=balance_date
        )

        try:
            obj = CarWashBank.objects.create(**ps)
            return 0, obj
        except Exception, e:
            print e
            return 99900, dict_err.get(99900)

    def search_banks_for_admin(self, car_wash_name):
        objs = CarWashBank.objects.select_related('car_wash').all()

        if car_wash_name:
            objs = objs.filter(car_wash__name__contains=car_wash_name)

        return objs

    def get_bank_by_id(self, bank_id, state=True):
        objs = CarWashBank.objects.filter(pk=bank_id)
        if state:
            objs.filter(state=state)
        return objs[0] if objs else None

    def modify_bank(self, bank_id, car_wash_id, manager_name, mobile, tel, bank_name, bank_card, balance_date):
        if not (bank_id, car_wash_id and manager_name and mobile
                and tel and bank_name and bank_card and balance_date):
            return 99800, dict_err.get(99800)

        obj = self.get_bank_by_id(bank_id, None)
        if not obj:
            return 20108, dict_err.get(20108)

        temp = self.get_bank_by_car_wash(car_wash_id)
        if temp and temp[0] != obj:
            return 20107, dict_err.get(20107)

        ps = dict(
            car_wash_id=car_wash_id,
            manager_name=manager_name,
            mobile=mobile,
            tel=tel,
            bank_name=bank_name,
            bank_card=bank_card,
            balance_date=balance_date
        )

        for k, v in ps.items():
            setattr(obj, k, v)

        try:
            obj.save()
        except:
            return 99900, dict_err.get(99900)

        return 0, dict_err.get(0)
