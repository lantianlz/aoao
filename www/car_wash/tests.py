# -*- coding: utf-8 -*-

import os
import sys

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
# 引入父目录来引入其他模块
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

import random
import datetime
from common import utils
from www.car_wash import interface

stb = interface.ServiceTypeBase()
cwb = interface.CarWashBase()
spb = interface.ServicePriceBase()
cb = interface.CouponBase()
ocb = interface.OrderCodeBase()
cwmb = interface.CarWashManagerBase()

city_id = 1974
district_id = 3247
business_hours = "09:00-18:00"
user_id = "d081652b603211e48a41685b35d0bf16"


def add_cw():
    datas = ([u"心愿洗车养护店", "13551828850", u"成都市高新区府城大道东段天长路104号", 0, "104.081363", "30.595177"],
             [u"成都高新区紫荆洗车站", "13551828850", u"成都市紫荆南路19号", 1, "104.057487", "30.621162"],
             [u"巧车匠汽车清洁护理", "69162992", u"高新区府城大道中段88号九方购物中心B2楼 ", 0, "104.072143", "30.595791"],
             )
    for data in datas:
        name, tel, addr, wash_type, longitude, latitude = data
        errcode, result = cwb.add_car_wash(city_id, district_id, name, business_hours, tel, addr,
                                           lowest_sale_price="10.00", lowest_origin_price="30.00", longitude=longitude, latitude=latitude, imgs="", wash_type=wash_type)
        print errcode, result.encode("utf8")


def add_sp():
    for car_wash in cwb.get_car_washs_by_city_id(city_id):
        print spb.add_service_price(car_wash=car_wash, service_type_id=1, sale_price=10, origin_price=20, clear_price=15)
        print spb.add_service_price(car_wash=car_wash, service_type_id=2, sale_price=20, origin_price=40, clear_price=25)


def add_cou():
    user_id = "d081652b603211e48a41685b35d0bf16"
    datas = [
        [0, 5, user_id, 0, ""],
        [0, 15, user_id, 0, ""],

        [1, 0, user_id, 0, ""],
        [1, 5, user_id, 0, ""],
        [1, 10, user_id, 0, ""],
    ]
    for data in datas:
        coupon_type, discount, user_id, minimum_amount, car_wash_id = data
        expiry_time = datetime.datetime.now() + datetime.timedelta(days=random.randint(30, 90))
        errcode, result = cb.add_coupon(coupon_type, discount, expiry_time, user_id, minimum_amount, car_wash_id)
        if errcode:
            print errcode, result.encode("utf8")


def add_cms():
    print cwmb.add_car_wash_manager(1, user_id)


def main():

    # add_cw()
    # add_sp()
    # add_cou()
    add_cms()


if __name__ == '__main__':
    main()
