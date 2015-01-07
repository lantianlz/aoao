# -*- coding: utf-8 -*-

import time
from django.http import HttpResponseRedirect  # HttpResponse,Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils
from www.misc.decorators import member_required, auto_select_template
from www.cash import interface

ucb = interface.UserCashBase()
ucrb = interface.UserCashRecordBase()
cob = interface.CashOrderBase()


def cash_index(request, template_name='mobile/cash/cash_index.html'):
    user_cash = ucb.get_user_cash_by_user_id(request.user.id)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@auto_select_template
def user_cash_record(request, template_name='mobile/cash/user_cash_record.html'):
    records = ucrb.get_records_by_user_id(request.user.id)
    user_cash = ucb.get_user_cash_by_user_id(request.user.id)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
@auto_select_template
def recharge(request, template_name='mobile/cash/recharge.html'):
    from common.alipay import alipay_mobile
    from common.weixinpay import weixinpay
    from www.account.interface import ExternalTokenBase
    
    user_cash = ucb.get_user_cash_by_user_id(request.user.id)

    if request.POST:
        pay_type = request.POST.get("pay_type")
        total_fee = request.POST.get("total_fee")

        errcode, errmsg = cob.create_order(request.user.id, pay_type, total_fee, ip=utils.get_clientip(request))
        if errcode == 0:
            order = errmsg

            if order.pay_type == 1:  # 支付宝支付
                alipay = alipay_mobile.Alipay()
                flag, token = alipay.get_token(subject=u"嗷嗷洗车充值", out_trade_no=order.trade_id,
                                               total_fee=order.pay_fee, out_user=order.user_id)
                if flag:
                    return HttpResponseRedirect(alipay.get_pay_url())
            if order.pay_type == 2:     # 微信支付
                weixinpay = weixinpay.Weixinpay()
                flag, prepay_id = weixinpay.get_prepay_id(body=u"嗷嗷洗车充值", out_trade_no=order.trade_id,
                                                          total_fee=int(order.pay_fee * 100),
                                                          openid=ExternalTokenBase().get_weixin_openid_by_user_id(order.user_id))
                # openid="oNYsJj1eg4fnU4tKLvH-f2IXlxJ4")
                if flag:
                    return HttpResponseRedirect("/car_wash/weixinpay?showwxpaytitle=1&prepay_id=%s&trade_id=%s" % (prepay_id, order.trade_id))

            err_msg = u'支付跳转异常，请联系嗷嗷客服人员'
            return render_to_response('error.html', locals(), context_instance=RequestContext(request))
        else:
            warning_msg = errmsg

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def bind_mobile(request, template_name='mobile/cash/bind_mobile.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def setting(request, template_name='mobile/cash/setting.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
