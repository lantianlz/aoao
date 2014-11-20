# -*- coding: utf-8 -*-

import datetime

from decimal import Decimal
from common import utils
from www.misc import consts

from www.account.interface import UserBase
from www.cash.models import UserCash, UserCashRecord, CarWashCash, CarWashRecord

dict_err = {
    30100: u'',
}
dict_err.update(consts.G_DICT_ERROR)


class UserCashBase(object):

    def get_user_cash_by_user_id(self, user_id):
        try:
            return UserCash.objects.get(user_id=user_id)
        except UserCash.DoesNotExist:
            return utils.DictLikeObject(user_id=user_id, balance=Decimal("0.00"))


class CarWashCashBase(object):

    def get_user_cash_by_user_id(self, car_wash_id):
        try:
            return CarWashCash.objects.get(car_wash_id=car_wash_id)
        except CarWashCash.DoesNotExist:
            return utils.DictLikeObject(car_wash_id=car_wash_id, balance=Decimal("0.00"))
