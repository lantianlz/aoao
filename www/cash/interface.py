# -*- coding: utf-8 -*-

import datetime
import logging
from decimal import Decimal
from django.db import transaction

from common import utils, debug
from www.misc import consts
from www.account.interface import UserBase
from www.cash.models import UserCash, UserCashRecord, CarWashCash, CarWashRecord

dict_err = {
    30100: u'',
}
dict_err.update(consts.G_DICT_ERROR)

DEFAULT_DB = 'default'


class UserCashBase(object):

    def get_user_cash_by_user_id(self, user_id):
        try:
            return UserCash.objects.get(user_id=user_id)
        except UserCash.DoesNotExist:
            return utils.DictLikeObject(user_id=user_id, balance=Decimal("0.00"))

    @transaction.commit_manually(using=DEFAULT_DB)
    def withdraw(self, user_id, value, notes):
        """
        @note:消费
        """
        try:
            try:
                value = int(value)
            except:
                transaction.rollback(using=DEFAULT_DB)
            if value < 0:
                transaction.rollback(using=DEFAULT_DB)
            if not allow_overdraft and (self.balance - value) < 0:
                transaction.rollback()
                raise Overdraft, u'overdraft'
            self.balance -= value
            UserCashRecord.create(value=value * -1, current_balance=self.balance, operation=operation, notes=notes)

            transaction.commit(using=DEFAULT_DB)
            return 0, dict_err.get(0)
        except Exception, e:
            logging.error(debug.get_debug_detail(e))
            transaction.rollback(using=DEFAULT_DB)
            return 99900, dict_err.get(99900)

    @transaction.commit_manually(using=DEFAULT_DB)
    def deposit(self, vuser_id, value, notes):
        """
        @note:充值
        """
        try:
            try:
                value = int(value)
            except:
                transaction.rollback()
                raise ValueError("Value must be a Python int")
            if value < 0:
                transaction.rollback()
                raise ValueError("You can't deposit a negative amount")
            self.balance += value
            t = self.transactions.create(
                date=datetime.datetime.now(),
                value=value,
                current_balance=self.balance,
                app=app,
                operation=operation,
                notes=notes,
            )
            self.save()
            transaction.commit()
            return t
        except Exception, e:
            logging.error(debug.get_debug_detail(e))
            transaction.rollback()
            raise e


class CarWashCashBase(object):

    def get_user_cash_by_user_id(self, car_wash_id):
        try:
            return CarWashCash.objects.get(car_wash_id=car_wash_id)
        except CarWashCash.DoesNotExist:
            return utils.DictLikeObject(car_wash_id=car_wash_id, balance=Decimal("0.00"))
