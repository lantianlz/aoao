# -*- coding: utf-8 -*-

import os
import sys

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
# 引入父目录来引入其他模块
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

from www.car_wash import interface


def main():
    stb = interface.ServiceTypeBase()
    cwb = interface.CarWashBase()
    spb = interface.ServicePriceBase()
    # print stb.add_service_type(name=u"标准洗车(5座)")
    # print stb.modify_service_type(1, u"标准洗车(5座)")
    # print spb.add_service_price(car_wash=1, service_type_id=1, sale_price=10, origin_price=30, clear_price=15)

    city_id = 1974
    district_id = 1978
    business_hours = "09:00-18:00"

    name, tel, addr, wash_type, longitude, latitude = u"心愿洗车养护店", "13551828850", u"成都市高新区府城大道东段天长路104号", 0, "104.081363", "30.595177"
    # name, tel, addr, wash_type, longitude, latitude = u"成都高新区紫荆洗车站", "13551828850", u"成都市紫荆南路19号", 1, "104.057487", "30.621162"
    print cwb.add_car_wash(city_id, district_id, name, business_hours, tel, addr,
                           lowest_sale_price="10.00", lowest_origin_price="30.00", longitude=longitude, latitude=latitude, imgs="", wash_type=wash_type)


if __name__ == '__main__':
    main()
