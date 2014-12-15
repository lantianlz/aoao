# -*- coding: utf-8 -*-

import json
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from www.misc.decorators import staff_required, common_ajax_response, verify_permission
from www.misc import qiniu_client
from common import utils, page
from www.custom_tags.templatetags.custom_filters import str_display

from www.account.interface import UserBase, ExternalTokenBase


@verify_permission('')
def active_user(request, template_name='pc/admin/statistics_active_user.html'):
    from www.account.models import LastActive
    sources = [{'value': x[0], 'name': x[1]} for x in LastActive.last_active_source_choices]
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@verify_permission('statistics_active_user')
def get_active_user(request):
    page_index = int(request.REQUEST.get('page_index', 1))

    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day)

    ub = UserBase()
    objs = ub.get_active_users(today)

    page_objs = page.Cpt(objs, count=10, page=page_index).info

    # 格式化
    format_users = [ub.format_user_full_info(x.user_id) for x in page_objs[0]]

    data = []
    num = 10 * (page_index - 1) + 0

    for user in format_users:

        num += 1
        data.append({
            'num': num,
            'user_id': user.id,
            'user_avatar': user.get_avatar_25(),
            'user_nick': user.nick,
            'user_email': user.email,
            'source': user.last_active_source,
            'user_des': str_display(user.des, 17),
            'last_active': str(user.last_active),
            'state': user.state,
            'ip': user.last_active_ip
        })

    return HttpResponse(
        json.dumps({'data': data, 'page_count': page_objs[4], 'total_count': page_objs[5]}),
        mimetype='application/json'
    )


@verify_permission('')
def external(request, template_name='pc/admin/statistics_external.html'):
    from www.account.models import ExternalToken
    source_choices = [{'value': x[0], 'name': x[1]} for x in ExternalToken.source_choices]
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@verify_permission('statistics_external')
def get_external(request):
    page_index = int(request.REQUEST.get('page_index', 1))

    s_date = request.REQUEST.get('s_date')
    s_date = (s_date if s_date else datetime.datetime.now().strftime('%Y-%m-%d')) + " 00:00:00"

    e_date = request.REQUEST.get('e_date')
    e_date = (e_date if e_date else datetime.datetime.now().strftime('%Y-%m-%d')) + " 00:00:00"

    objs = ExternalTokenBase().get_external_for_admin(s_date, e_date)

    page_objs = page.Cpt(objs, count=10, page=page_index).info

    data = []
    num = 10 * (page_index - 1) + 0

    for x in page_objs[0]:

        num += 1

        user = UserBase().get_user_by_id(x.user_id) if x.user_id else None

        data.append({
            'num': num,
            'external_id': x.id,
            'user_id': x.user_id if user else '',
            'user_nick': user.nick if user else '',
            'source': x.source,
            'access_token': x.access_token,
            'refresh_token': x.refresh_token,
            'external_user_id': x.external_user_id,
            'union_id': x.union_id,
            'app_id': x.app_id,
            'nick': x.nick,
            'user_url': x.user_url,
            'expire_time': str(x.expire_time),
            'create_time': str(x.create_time),
            'update_time': str(x.update_time),
            'state': x.state
        })

    return HttpResponse(
        json.dumps({'data': data, 'page_count': page_objs[4], 'total_count': page_objs[5]}),
        mimetype='application/json'
    )
