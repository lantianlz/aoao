# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse, Http404  # , HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response


def cash_index(request, template_name='mobile/car_wash/account.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def record_deal(request, template_name='mobile/car_wash/record_deal.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def pay(request, template_name='mobile/car_wash/pay.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
