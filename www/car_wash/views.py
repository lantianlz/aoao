# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse  # , HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request, template_name='mobile/car_wash/index.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def detail(request, car_wash_id=None, template_name='mobile/car_wash/detail.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def order(request, province_id=None, template_name='mobile/car_wash/order.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def order_detail(request, order_detail_id=None, template_name="mobile/car_wash/order_detail.html"):

	return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def coupon(request, template_name='mobile/car_wash/coupon.html'):

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