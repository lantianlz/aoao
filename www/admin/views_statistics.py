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

@verify_permission('')
def retention(request, template_name='pc/admin/statistics_retention.html'):
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
            'user_avatar': user.get_avatar_65(),
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