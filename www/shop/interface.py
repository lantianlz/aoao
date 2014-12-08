# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from www.car_wash.interface import CarWashManagerBase


def car_wash_manager_required_for_request(func):
    """
    @note: 过滤器, 商户后台使用
    """
    def _decorator(request, car_wash_id, *args, **kwargs):
        cwm = CarWashManagerBase().get_cwm_by_car_wash_and_user_id(car_wash_id, request.user.id)
        if not cwm:
            err_msg = u'权限不足，你还不是嗷嗷商户管理员，如有疑问请联系嗷嗷客服'
            return render_to_response('error.html', locals(), context_instance=RequestContext(request))
        request.car_wash = cwm.car_wash
        return func(request, car_wash_id, *args, **kwargs)
    return _decorator
