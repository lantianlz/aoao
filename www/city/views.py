# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse  # , HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from www.city.interface import CityBase


def show_open_citys(request, template_name='mobile/city/open_citys_list.html'):
    cb = CityBase()

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def provinces(request, template_name='mobile/city/provinces.html'):
    cb = CityBase()

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def cities(request, province_id=None, template_name='mobile/city/cities.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
