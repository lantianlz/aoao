# -*- coding: utf-8 -*-

import logging

from django.utils.encoding import smart_str
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from pyquery import PyQuery as pq

from common import debug
from common.alipay import alipay_mobile
from www.car_wash.interface import OrderBase


def alipaycallback_m(request):
    """
    @note: 支付宝手机支付回调，页面跳转方式
    仅做检测，不做后续处理，由服务器通知方式进行后续处理，避免同时并发的方式
    """
    logging.error(u"alipaycallback_m info is: %s" % smart_str(request.REQUEST))

    alipay = alipay_mobile.Alipay()
    flag = alipay.validate_html_redirect_params(request)
    if flag:
        timeinterval = 3
        next_url = "/"  # 成功跳转url控制
        if request.REQUEST.get("out_trade_no", "").startswith("W"):
            next_url = "/car_wash/order_code"
        if request.REQUEST.get("out_trade_no", "").startswith("R"):
            next_url = "/cash"

        success_msg = u'支付成功，页面即将跳转'
        return render_to_response('success.html', locals(), context_instance=RequestContext(request))
    else:
        err_msg = u'支付结果校验异常，请联系嗷嗷客服人员'
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))


def alipaynotify_m(request):
    """
    @note: 支付宝手机支付通知，服务器通知方式
    """
    logging.error(u"alipaynotify_m info is: %s" % smart_str(request.REQUEST))

    alipay = alipay_mobile.Alipay()
    flag = alipay.validate_notify_params(request)
    result = 'fail'
    if flag:
        notify_data = request.REQUEST.get('notify_data', '')
        jq = pq(notify_data)
        trade_status = jq('trade_status').html()

        if trade_status in ('TRADE_FINISHED', 'TRADE_SUCCESS'):
            trade_no = jq('trade_no').html()
            buyer_email = jq('buyer_email').html()
            buyer_id = jq('buyer_id').html()
            trade_id = jq('out_trade_no').html()
            total_fee = float(jq('total_fee').html())
            pay_info = 'trade_no:%s, buyer_email:%s, buyer_id:%s' % (trade_no, buyer_email, buyer_id)

            # print pay_info
            # print trade_id
            # print total_fee

            if trade_id.startswith("W"):
                errcode, errmsg = OrderBase().order_pay_callback(trade_id=trade_id, payed_fee=total_fee, pay_info=pay_info)
                result = u'success' if errcode in (0, 20301) else 'fail'  # 不存在的订单返回成功防止一直补发

    return HttpResponse(result)


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
    return HttpResponse("not the one who can test")
