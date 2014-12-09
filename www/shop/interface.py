# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from www.car_wash.interface import CarWashBase, CarWashManagerBase


def car_wash_manager_required_for_request(func):
    """
    @note: 过滤器, 商户后台使用
    """
    def _decorator(request, car_wash_id, *args, **kwargs):
        is_cwm = CarWashManagerBase().check_user_is_cwm(car_wash_id, request.user)
        if not is_cwm:
            if request.is_ajax():
                return HttpResponse('{}')
            err_msg = u'权限不足，你还不是嗷嗷商户管理员，如有疑问请联系嗷嗷客服'
            return render_to_response('error.html', locals(), context_instance=RequestContext(request))

        car_wash = CarWashBase().get_car_wash_by_id(car_wash_id)
        if not car_wash:
            raise Http404

        request.car_wash = car_wash
        return func(request, car_wash, *args, **kwargs)
    return _decorator
