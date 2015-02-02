# -*- coding: utf-8 -*-

import json
import datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, page
from www.misc.decorators import member_required, common_ajax_response, auto_select_template

from www.cash.interface import CarWashCashBase, CarWashCashRecordBase
from www.shop.interface import car_wash_manager_required_for_request

from www.car_wash import interface
cwmb = interface.CarWashManagerBase()
ocb = interface.OrderCodeBase()


def login_shop(request, template_name='pc/shop/login_shop.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
def shop_index(request):

    # 判断是否是公司管理员
    cm = interface.CompanyManagerBase().get_cm_by_user_id(request.user.id)
    if cm:
        return HttpResponseRedirect("/company/%s/shop_list" % cm.company.id)

    # 是否是商户管理员
    cwm = cwmb.get_cwm_by_user_id(request.user.id)
    if cwm:
        return HttpResponseRedirect("/shop/%s/verify_code" % cwm.car_wash.id)

    err_msg = u'权限不足，你还不是嗷嗷商户管理员，如有疑问请联系嗷嗷客服'
    return render_to_response('error.html', locals(), context_instance=RequestContext(request))


@member_required
@auto_select_template
@car_wash_manager_required_for_request
def verify_code(request, car_wash_id, template_name):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
@car_wash_manager_required_for_request
def shop_cash(request, car_wash_id, template_name='pc/shop/shop_cash.html'):
    car_wash_cash = CarWashCashBase().get_car_wash_cash_by_car_wash_id(car_wash_id)
    end_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    start_date = datetime.datetime.strptime('%s-%s-01' % (end_date.year, end_date.month), '%Y-%m-%d').date()

    if request.POST.get("start_date"):
        end_date = datetime.datetime.strptime(request.POST.get("end_date"), '%Y-%m-%d').date()
        start_date = datetime.datetime.strptime(request.POST.get("start_date"), '%Y-%m-%d').date()

    records = CarWashCashRecordBase().get_records_by_range_date(car_wash_id, start_date, end_date)
    in_reords = CarWashCashRecordBase().get_records_by_range_date(car_wash_id, start_date, end_date, operation=0)
    in_reords_count = in_reords.count()
    total_fee = sum([r.value for r in in_reords])

    # 分页
    page_count = 20
    page_num = int(request.REQUEST.get('page', 1))
    page_objs = page.Cpt(records, count=page_count, page=page_num).info
    page_params = (page_objs[1], page_objs[4])
    records = page_objs[0]

    _format_objs_set_index(records, page_num, page_count)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@member_required
@car_wash_manager_required_for_request
def chart(request, car_wash_id, template_name='pc/shop/chart.html'):
    car_wash_cash = CarWashCashBase().get_car_wash_cash_by_car_wash_id(car_wash_id)
    end_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    start_date = datetime.datetime.strptime('%s-%s-01' % (end_date.year, end_date.month), '%Y-%m-%d').date()

    if request.POST.get("start_date"):
        end_date = datetime.datetime.strptime(request.POST.get("end_date"), '%Y-%m-%d').date()
        start_date = datetime.datetime.strptime(request.POST.get("start_date"), '%Y-%m-%d').date()

    in_reords = CarWashCashRecordBase().get_records_by_range_date(car_wash_id, start_date, end_date, operation=0)
    in_reords_count = in_reords.count()
    total_fee = sum([r.value for r in in_reords])

    dict_records = CarWashCashRecordBase().format_records_with_day(in_reords)
    days = []
    values = []
    _start_date = start_date
    while _start_date <= end_date:
        days.append(str(_start_date))
        values.append(dict_records.get(str(_start_date), "0.00"))
        _start_date += datetime.timedelta(days=1)

    days = json.dumps(days)
    values = json.dumps(values)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def _format_objs_set_index(objs, page_num, page_count):
    """
    @note: 格式化对象，设置index值
    """
    for i, obj in enumerate(objs):
        obj.index = (page_num - 1) * page_count + i + 1


@auto_select_template
def help(request, template_name='pc/shop/help.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
# ===================================================ajax部分=================================================================#

@member_required
@car_wash_manager_required_for_request
def get_order_code(request, car_wash_id):
    code = request.REQUEST.get("code", "").strip().replace(" ", "")
    order_code = ocb.get_order_code_by_car_wash_and_code(request.car_wash, code)

    data = {}
    if order_code:
        service_price = order_code.order.service_price
        user = order_code.get_user()
        data = dict(code=order_code.get_code_display(), car_wash_name=order_code.car_wash.name,
                    sale_price=service_price.sale_price, clear_price=service_price.clear_price,
                    state=order_code.state, state_display=order_code.get_state_display(),
                    pay_time=order_code.order.pay_time.strftime('%Y-%m-%d %H:%M'),
                    user_nick=user.nick, service_type_name=service_price.service_type.name,
                    use_time=order_code.use_time.strftime('%Y-%m-%d %H:%M') if order_code.use_time else '')
    return HttpResponse(json.dumps(data))


@member_required
@car_wash_manager_required_for_request
@common_ajax_response
def use_order_code(request, car_wash_id):
    code = request.REQUEST.get("code", "").strip().replace(" ", "")
    return ocb.use_order_code(request.car_wash, request.user, code, ip=utils.get_clientip(request))
