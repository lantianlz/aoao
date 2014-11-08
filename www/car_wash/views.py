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


def coupon(request, province_id=None, template_name='mobile/car_wash/coupon.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))