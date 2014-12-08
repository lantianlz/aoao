# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, user_agent_parser, page
from www.misc.decorators import member_required
from www.shop.interface import car_wash_manager_required_for_request

from www.car_wash import interface
cwmb = interface.CarWashManagerBase()


def login_shop(request, template_name='pc/shop/login_shop.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def shop_index(request):
    cwm = cwmb.get_cwm_by_user_id(request.user.id)
    if not cwm:
        err_msg = u'权限不足，你还不是嗷嗷商户管理员，如有疑问请联系嗷嗷客服'
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))

    return HttpResponseRedirect("/shop/%s/verify_code" % cwm.car_wash.id)


@member_required
@car_wash_manager_required_for_request
def verify_code(request, car_wash_id, template_name='pc/shop/verify_code.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def orders(request, template_name='pc/shop/orders.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def chart(request, template_name='pc/shop/chart.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
