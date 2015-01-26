# -*- coding: utf-8 -*-

import time
import json
import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from common import page, utils
from www.misc.decorators import member_required, common_ajax_response, auto_select_template
from www.city.interface import CityBase
from www.cash.interface import CarWashCashBase, CarWashCashRecordBase
from www.car_wash import interface
from www.car_wash.interface import company_manager_required_for_request

cwb = interface.CarWashBase()
spb = interface.ServicePriceBase()
cb = interface.CouponBase()
ob = interface.OrderBase()
ocb = interface.OrderCodeBase()
cmb = interface.CompanyManagerBase()


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
    from common.weixinpay import weixinpay
    from www.account.interface import ExternalTokenBase

    service_price = spb.get_service_price_by_id(service_price_id)
    if not service_price:
        raise Http404

    coupon_id = request.POST.get("coupon_id")
    coupon_id = None if coupon_id == "0" else coupon_id
    count = request.POST.get("count")
    use_user_cash = True if request.POST.has_key("use_user_cash") else False
    pay_type = request.POST.get("pay_type")
    page_show_pay_fee = request.POST.get("page_show_pay_fee")

    errcode, errmsg = ob.create_order(service_price, request.user.id, count,
                                      pay_type, coupon_id, use_user_cash, ip=utils.get_clientip(request), page_show_pay_fee=page_show_pay_fee)

    if errcode == 0:
        order = errmsg
        if order.pay_fee == 0:
            return HttpResponseRedirect("/car_wash/order_code")

        if order.pay_type == 1:  # 支付宝支付
            alipay = alipay_mobile.Alipay()
            flag, token = alipay.get_token(subject=u"嗷嗷洗车订单", out_trade_no=order.trade_id,
                                           total_fee=order.pay_fee, out_user=order.user_id)
            if flag:
                return HttpResponseRedirect(alipay.get_pay_url())
        if order.pay_type == 2:     # 微信支付
            weixinpay = weixinpay.Weixinpay()
            flag, prepay_id = weixinpay.get_prepay_id(body=u"嗷嗷洗车订单", out_trade_no=order.trade_id,
                                                      total_fee=int((order.pay_fee + 0.001) * 100),  # 避免0.01转换为0的结果
                                                      openid=ExternalTokenBase().get_weixin_openid_by_user_id(order.user_id))
            # openid="oNYsJj1eg4fnU4tKLvH-f2IXlxJ4")
            if flag:
                return HttpResponseRedirect("/car_wash/weixinpay?showwxpaytitle=1&prepay_id=%s&trade_id=%s" % (prepay_id, order.trade_id))

        err_msg = u'支付跳转异常，请联系嗷嗷客服人员'
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))
    else:
        warning_msg = errmsg
        return show_create_order(request, service_price_id, warning_msg)


@member_required
def weixinpay(request, template_name='mobile/car_wash/weixinpay.html'):
    """
    @note: 微信支付过渡页面，微信对支付目录有要求
    """
    from common.weixinpay import weixinpay

    prepay_id = request.REQUEST.get("prepay_id")
    trade_id = request.REQUEST.get("trade_id")
    weixinpay = weixinpay.Weixinpay()
    params = dict(appId=weixinpay.appid, timeStamp=int(time.time()), nonceStr=utils.uuid_without_dash(),
                  package="prepay_id=%s" % prepay_id, signType="MD5")   # 支付签名的参数不可改动
    params, prestr = weixinpay.format_params(params)
    sign = weixinpay.build_mysign(prestr)

    params["paySign"] = sign
    params["trade_id"] = trade_id

    return render_to_response(template_name, params, context_instance=RequestContext(request))


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

#@auto_select_template
def map(request, template_name="mobile/car_wash/map.html"):
    city_id = request.user.get_city_id() if request.user.is_authenticated() else request.session.get("city_id", 1974)
    city = CityBase().get_city_by_id(city_id)

    car_washs = cwb.get_car_washs_by_city_id(city_id)

    data = []

    for x in car_washs:

        # 过滤测试洗车行
        if not settings.LOCAL_FLAG and x.id == 1:
            continue

        data.append({
            'longitude': x.longitude, 
            'latitude': x.latitude, 
            'name': x.name, 
            'id': x.id, 
            'tel': x.tel, 
            'address': x.addr, 
            'lowestSalePrice': str(x.lowest_sale_price),
            'lowest_origin_price': str(x.lowest_origin_price)
        })

    data_json = json.dumps(data)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def company_index(request):
    cm = cmb.get_cm_by_user_id(request.user.id)
    if not cm:
        err_msg = u'权限不足，你还不是嗷嗷商户管理员，如有疑问请联系嗷嗷客服'
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))

    return HttpResponseRedirect("/company/%s/shop_list" % cm.company.id)

@member_required
@company_manager_required_for_request
def shop_list_of_company(request, company_id, template_name='pc/company/shop_list.html'):

    name = request.REQUEST.get('name', '')

    car_washs = cwb.get_car_wash_by_company_id(company_id, name)
    car_washs_count = car_washs.count()

    for x in car_washs:
        x.balance = CarWashCashBase().get_car_wash_cash_by_car_wash_id(x.id).balance

    # 分页
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(car_washs, count=10, page=page_num).info
    car_washs = page_objs[0]
    page_params = (page_objs[1], page_objs[4])

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
@company_manager_required_for_request
def company_cash(request, company_id, template_name='pc/company/company_cash.html'):
    end_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    start_date = datetime.datetime.strptime('%s-%s-01' % (end_date.year, end_date.month), '%Y-%m-%d').date()

    if request.POST.get("start_date"):
        end_date = datetime.datetime.strptime(request.POST.get("end_date"), '%Y-%m-%d').date()
        start_date = datetime.datetime.strptime(request.POST.get("start_date"), '%Y-%m-%d').date()

    records = CarWashCashRecordBase().get_company_records_by_range_date(company_id, start_date, end_date)
    in_reords = CarWashCashRecordBase().get_company_records_by_range_date(company_id, start_date, end_date, operation=0)
    in_reords_count = in_reords.count()
    total_fee = sum([r.value for r in in_reords])

    # 分页
    page_count = 20
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(records, count=page_count, page=page_num).info
    page_params = (page_objs[1], page_objs[4])
    records = page_objs[0]

    count = (page_num - 1) * page_count
    for x in records:
        count += 1

        car_wash = cwb.get_car_wash_by_id(x.car_wash_cash.car_wash_id)

        x.index = count
        x.car_wash_name = car_wash.name

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


@member_required
#@common_ajax_response
def refund_order(request, trade_id):
    #return ob.refund_order(trade_id)

    trade = ob.get_order_by_trade_id(trade_id)
    if not trade or trade.user_id != request.user.id:
        err_msg = u"此订单不属于你"
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))

    flag, msg = ob.refund_order(trade_id)

    if flag == 0:
        success_msg = u"订单 [%s] 退款成功" % trade_id
        next_url = "/car_wash/order/%s" % trade_id
        timeinterval = 3
        return render_to_response('success.html', locals(), context_instance=RequestContext(request))
    else:
        err_msg = msg
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))
