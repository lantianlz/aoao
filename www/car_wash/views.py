# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse, Http404  # , HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from www.misc.decorators import member_required
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

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def car_wash_detail(request, car_wash_id=None, template_name='mobile/car_wash/detail.html'):
    car_wash = cwb.get_car_wash_by_id(car_wash_id)
    if not car_wash:
        raise Http404
    service_prices = spb.get_service_prices_by_car_wash(car_wash)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# @member_required
def order(request, province_id=None, template_name='mobile/car_wash/order.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# @member_required
def order_detail(request, order_detail_id=None, template_name="mobile/car_wash/order_detail.html"):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# @member_required
def coupon(request, template_name='mobile/car_wash/coupon.html'):
    coupons = cb.get_coupons_by_user_id(request.user.id)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def account(request, template_name='mobile/car_wash/account.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def record_deal(request, template_name='mobile/car_wash/record_deal.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def bind_mobile(request, template_name='mobile/car_wash/bind_mobile.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def about(request, template_name='mobile/car_wash/about.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def setting(request, template_name='mobile/car_wash/setting.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def pay(request, template_name='mobile/car_wash/pay.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def buy(request, template_name='mobile/car_wash/buy.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def location(request, template_name='mobile/car_wash/location.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
