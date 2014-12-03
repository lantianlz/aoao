# -*- coding: utf-8 -*-


from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from common import debug
from www.car_wash.interface import OrderBase


def alipaycallback_m(request):
    """
    @note: 支付宝手机支付回调
    """
    pass


def alipaynotify_m(request):
    """
    @note: 支付宝手机支付通知
    """
    pass


def weixinpaycallback(request):
    """
    @note: 微信支付回调
    """
    pass


def test_paycallback(request):
    """
    @note: 测试回调
    """
    params = request.REQUEST

    if request.user.id in (u'd081652b603211e48a41685b35d0bf16',):
        buyer_email = params.get('buyer_email')
        buyer_id = params.get('buyer_id')
        trade_no = params.get('trade_no')
        trade_id = params.get('out_trade_no')
        total_fee = float(params.get('total_fee'))

        errcode, errmsg = 0, "支付成功"
        try:
            ob = OrderBase()
            pay_info = 'trade_no:%s, buyer_email:%s, buyer_id:%s' % (trade_no, buyer_email, buyer_id)
            errcode, errmsg = ob.order_pay_callback(trade_id=trade_id, payed_fee=total_fee, pay_info=pay_info)

            status = u'success' if errcode == 0 else 'fail'
        except Exception, e:
            debug.get_debug_detail(e)
            status = u'fail'
            errmsg = u'支付遇到问题: %s' % str(e)

        if errcode == 20301:    # 不存在的订单返回成功防止一直补发
            return HttpResponse('success')

        return HttpResponse(u"status is:%s\nerrmsg is:%s" % (status, errmsg))
    return HttpResponse("not the one")
