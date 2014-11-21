# -*- coding: utf-8 -*-

import json
import urllib
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, page
from misc.decorators import staff_required, common_ajax_response, verify_permission

from www.car_wash.interface import CarWashBase

@verify_permission('')
def car_wash(request, template_name='pc/admin/car_wash.html'):
    from www.car_wash.models import CarWash
    wash_type_choices = [{'name': x[1], 'value': x[0]} for x in CarWash.wash_type_choices]

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def format_car_wash(objs, num):
    data = []

    for x in objs:
        num += 1
        data.append({
            'num': num,
            'car_wash_id': x.id,
            'name': x.name,
            'business_hours': x.business_hours,
            'city_id': x.city_id,
            'city_name': '',
            'district_id': x.district_id,
            'district_name': '',
            'tel': x.tel,
            'addr': x.addr,
            'longitude': x.longitude,
            'latitude': x.latitude,
            'wash_type': x.wash_type,
            'des': x.des,
            'note': x.note,
            'lowest_sale_price': x.lowest_sale_price,
            'lowest_origin_price': x.lowest_origin_price,
            'imgs': x.imgs,
            'rating': x.rating,
            'order_count': x.order_count,
            'valid_date_start': str(x.valid_date_start),
            'valid_date_end': str(x.valid_date_end),
            'is_vip': x.is_vip,
            'vip_info': x.vip_info,
            'sort_num': x.sort_num,
            'state': x.state,
            'create_time': str(x.create_time)
        })

    return data


@verify_permission('query_user')
def search(request):
    name = request.REQUEST.get('name')
    page_index = int(request.REQUEST.get('page_index', 1))

    objs = CarWashBase().search_car_washs_for_admin(name)

    page_objs = page.Cpt(objs, count=10, page=page_index).info

    # 格式化json
    num = 10 * (page_index - 1)
    data = format_car_wash(page_objs[0], num)

    return HttpResponse(
        json.dumps({'data': data, 'page_count': page_objs[4], 'total_count': page_objs[5]}),
        mimetype='application/json'
    )


@verify_permission('query_user')
def get_car_wash_by_id(request):
    user_id = request.REQUEST.get('user_id')
    data = ''

    user = UserBase().get_user_by_id(user_id)
    if user:
        user = UserBase().format_user_full_info(user.id)

        data = {
            'user_id': user.id,
            'user_avatar': user.get_avatar_25(),
            'user_avatar_300': user.get_avatar_300(),
            'user_nick': user.nick,
            'user_des': user.des,
            'user_email': user.email,
            'user_gender': user.gender,
            'birthday': str(user.birthday),
            'is_admin': user.is_admin,
            'last_active': str(user.last_active),
            'state': user.state,
            'source': user.source_display,
            'ip': user.ip,
            'register_date': str(user.create_time)
        }

    return HttpResponse(json.dumps(data), mimetype='application/json')


@verify_permission('modify_user')
@common_ajax_response
def modify_car_wash(request):

    user_id = request.REQUEST.get('user_id')
    nick = request.REQUEST.get('nick')
    gender = request.REQUEST.get('gender')
    birthday = request.REQUEST.get('birthday')
    des = request.REQUEST.get('des')
    state = int(request.REQUEST.get('state'))

    user = UserBase().get_user_by_id(user_id)

    return UserBase().change_profile(user, nick, gender, birthday, des, state)
