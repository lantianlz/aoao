# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from www.city.interface import CityBase

cb = CityBase()


def open_citys_list(request, template_name='mobile/city/open_citys_list.html'):
    citys = cb.get_all_show_citys()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def provinces_list(request, template_name='mobile/city/provinces_list.html'):
    provinces = cb.get_all_provinces()
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def citys_list(request, province_id, template_name='mobile/city/citys_list.html'):
    province = cb.get_province_by_id(province_id)
    if not province:
        raise Http404
    citys = cb.get_citys_by_province(province_id=province_id, is_show=False)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
