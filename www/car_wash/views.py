# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import page
# from www.misc.decorators import member_required, common_ajax_response
from www.city.interface import CityBase
from www.car_wash import interface

cwb = interface.CarWashBase()
spb = interface.ServicePriceBase()
cb = interface.CouponBase()


def index(request, template_name='mobile/car_wash/index.html'):
    city_id = request.user.get_city_id() if request.user.is_authenticated() else request.session.get("city_id", 1974)
    city = CityBase().get_city_by_id(city_id)

    order_by_value = request.REQUEST.get("order_by_value", "0")
    car_washs = cwb.get_car_washs_by_city_id(city_id, order_by_value)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(car_washs, count=10, page=page_num).info
    car_washs = page_objs[0]

    is_show_more_flag = True if page_objs[1] < page_objs[4] else False  # 是否展示更多按钮

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def car_wash_detail(request, car_wash_id=None, template_name='mobile/car_wash/detail.html'):
    car_wash = cwb.get_car_wash_by_id(car_wash_id)
    if not car_wash:
        raise Http404
    service_prices = spb.get_service_prices_by_car_wash(car_wash)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def my_coupons(request, template_name='mobile/car_wash/coupon.html'):
    coupons = cb.get_coupons_by_user_id(request.user.id)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def show_create_order(request, service_price_id, template_name='mobile/car_wash/create_order.html'):
    from www.cash.interface import UserCashBase

    service_price = spb.get_service_price_by_id(service_price_id)
    if not service_price:
        raise Http404

    user_cash = UserCashBase().get_user_cash_by_user_id(request.user.id)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def order(request, province_id=None, template_name='mobile/car_wash/order.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def order_detail(request, order_detail_id=None, template_name="mobile/car_wash/order_detail.html"):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def location(request, template_name='mobile/car_wash/location.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# ===================================================ajax部分=================================================================#


def bind_mobile(request, template_name='mobile/car_wash/bind_mobile.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def setting(request, template_name='mobile/car_wash/setting.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def get_car_washs(request):

    city_id = request.user.get_city_id() if request.user.is_authenticated() else request.session.get("city_id", 1974)
    order_by_value = request.REQUEST.get("order_by_value", "0")
    car_washs = cwb.get_car_washs_by_city_id(city_id, order_by_value)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(car_washs, count=10, page=page_num).info
    car_washs = cwb.format_car_washs_for_ajax(page_objs[0])

    return HttpResponse(json.dumps(car_washs))
