# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import page, utils
from www.misc.decorators import member_required
from www.city.interface import CityBase
from www.car_wash import interface

cwb = interface.CarWashBase()
spb = interface.ServicePriceBase()
cb = interface.CouponBase()
ob = interface.OrderBase()
ocb = interface.OrderCodeBase()


def index(request, template_name='mobile/car_wash/index.html'):
    city_id = request.user.get_city_id() if request.user.is_authenticated() else request.session.get("city_id", 1974)
    city = CityBase().get_city_by_id(city_id)

    order_by_value = request.REQUEST.get("order_by_value") or "0"
    car_washs = cwb.get_car_washs_by_city_id(city_id, order_by_value)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(car_washs, count=10, page=page_num).info
    car_washs = page_objs[0]

    is_show_more_flag = True if page_objs[1] < page_objs[4] else False  # 是否展示更多按钮

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def car_wash_detail(request, car_wash_id=None, template_name='mobile/car_wash/car_wash_detail.html'):
    car_wash = cwb.get_car_wash_by_id(car_wash_id)
    if not car_wash:
        raise Http404
    service_prices = spb.get_service_prices_by_car_wash(car_wash)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def my_coupons(request, template_name='mobile/car_wash/coupon.html'):
    coupons = cb.get_coupons_by_user_id(request.user.id)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def show_create_order(request, service_price_id, warning_msg=None, template_name='mobile/car_wash/show_create_order.html'):
    """
    @note: 显示创建订单页面
    """
    from www.cash.interface import UserCashBase

    service_price = spb.get_service_price_by_id(service_price_id)
    if not service_price:
        raise Http404

    user_cash = UserCashBase().get_user_cash_by_user_id(request.user.id)
    coupons = cb.get_valid_coupon_by_user_id(request.user.id)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def create_order(request, service_price_id, template_name='mobile/car_wash/show_create_order.html'):
    """
    @note: 创建订单
    """
    from common.alipay import alipay_mobile

    service_price = spb.get_service_price_by_id(service_price_id)
    if not service_price:
        raise Http404

    coupon_id = request.POST.get("coupon_id")
    coupon_id = None if coupon_id == "0" else coupon_id
    count = request.POST.get("count")
    use_user_cash = True if request.POST.has_key("use_user_cash") else False
    pay_type = 2 if request.POST.has_key("pay_type_weixin") else 1
    pay_type = 1 if request.POST.has_key("pay_type_alipay") else 2
    page_show_pay_fee = request.POST.get("page_show_pay_fee")

    errcode, errmsg = ob.create_order(service_price, request.user.id, count,
                                      pay_type, coupon_id, use_user_cash, ip=utils.get_clientip(request), page_show_pay_fee=page_show_pay_fee)

    if errcode == 0:
        order = errmsg
        if order.pay_fee == 0:
            return HttpResponseRedirect("/car_wash/order_code")

        if order.pay_type == 1:  # 支付宝支付
            alipay = alipay_mobile.Alipay()
            flag, token = alipay.get_token(subject=u"%s洗车服务" % order.car_wash.name, out_trade_no=order.trade_id,
                                           total_fee=order.pay_fee, out_user=order.user_id)
            if flag:
                return HttpResponseRedirect(alipay.get_pay_url())
        if order.pay_type == 2:     # 微信支付
            pass

        err_msg = u'支付跳转异常，请联系嗷嗷客服人员'
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))
    else:
        warning_msg = errmsg
        return show_create_order(request, service_price_id, warning_msg)


def order_code(request, province_id=None, template_name='mobile/car_wash/order_code_list.html'):
    is_valid = request.REQUEST.get("is_valid") or "1"
    if is_valid == "1":
        codes = ocb.get_valid_order_codes_by_user_id(request.user.id)
    else:
        codes = ocb.get_complete_order_codes_by_user_id(request.user.id)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def order_detail(request, trade_id, template_name="mobile/car_wash/order_detail.html"):
    order = ob.get_order_by_trade_id(trade_id)
    if not order:
        raise Http404

    if order.user_id != request.user.id:  # 自己才能看自己的订单
        err_msg = u'what are you doing? 别人的订单不要看哦'
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))

    codes = ocb.get_order_codes_by_order(order)
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def location(request, template_name='mobile/car_wash/location.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# ===================================================ajax部分=================================================================#


def get_car_washs(request):

    city_id = request.user.get_city_id() if request.user.is_authenticated() else request.session.get("city_id", 1974)
    order_by_value = request.REQUEST.get("order_by_value", "0")
    car_washs = cwb.get_car_washs_by_city_id(city_id, order_by_value)

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(car_washs, count=10, page=page_num).info
    car_washs = cwb.format_car_washs_for_ajax(page_objs[0])

    return HttpResponse(json.dumps(car_washs))
