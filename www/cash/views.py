# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404  # , HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response


from www.cash import interface
ucb = interface.UserCashBase()


def cash_index(request, template_name='mobile/cash/cash_index.html'):
    user_cash = ucb.get_user_cash_by_user_id(request.user.id)

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def user_cash_record(request, template_name='mobile/cash/user_cash_record.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def recharge(request, template_name='mobile/cash/recharge.html'):

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))
