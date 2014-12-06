# -*- coding: utf-8 -*-

import urllib
import json
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response

from common import utils, user_agent_parser, page
from www.misc import qiniu_client
from www.misc.decorators import member_required

def login_shop(request, template_name='pc/shop/login_shop.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def verify_code(request, template_name='pc/shop/verify_code.html'):
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))