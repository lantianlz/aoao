# -*- coding: utf-8 -*-

import time
import random
import requests
import json
import logging
from django.conf import settings

from common import cache, debug
from www.misc import consts

from www.car_wash.models import CarWash, ServicePrice, ServiceType

dict_err = {
    20100: u'',
}
dict_err.update(consts.G_DICT_ERROR)


class CarWashBase(object):

    def __init__(self):
        pass

    def __del__(self):
        pass
