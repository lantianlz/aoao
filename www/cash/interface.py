# -*- coding: utf-8 -*-

import logging
from decimal import Decimal
from django.db import transaction

from common import utils, debug
from www.misc import consts
from www.account.interface import UserBase
from www.car_wash.interface import car_wash_required
from www.cash.models import UserCash, UserCashRecord, CarWashCash, CarWashCashRecord

dict_err = {
    30100: u'余额不足',
}
dict_err.update(consts.G_DICT_ERROR)

DEFAULT_DB = 'default'


class UserCashBase(object):

    def get_user_cash_by_user_id(self, user_id, auto_create_obj=False):
        try:
            return UserCash.objects.get(user_id=user_id)
        except UserCash.DoesNotExist:
            if not auto_create_obj:
                return utils.DictLikeObject(user_id=user_id, balance=Decimal("0.00"))
            else:
                return UserCash.objects.create(user_id=user_id)


class UserCashRecordBase(object):

    def validate_record_info(self, user_id, value, operation, notes):
        value = float(value)
        operation = int(operation)
        user = UserBase().get_user_by_id(user_id)
        assert operation in (0, 1)
        assert value > 0 and notes and user

    @transaction.commit_manually(using=DEFAULT_DB)
    def add_record_with_transaction(self, user_id, value, operation, notes, ip=None):
        try:
            errcode, errmsg = self.add_record(user_id, value, operation, notes, ip)
            if errcode == 0:
                transaction.commit(using=DEFAULT_DB)
            else:
                transaction.rollback(using=DEFAULT_DB)
            return errcode, errmsg
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=DEFAULT_DB)
            return 99900, dict_err.get(99900)

    def add_record(self, user_id, value, operation, notes, ip=None):
        """
        @note: 流水记录, operation:0为转入，1为转出
        """
        try:
            try:
                value = Decimal(value)
                operation = int(operation)
                self.validate_record_info(user_id, value, operation, notes)
            except Exception, e:
                return 99801, dict_err.get(99801)

            user_cash = UserCashBase().get_user_cash_by_user_id(user_id, auto_create_obj=True)

            if operation == 1 and user_cash.balance - value < 0:
                return 30100, dict_err.get(30100)

            if operation == 0:
                user_cash.balance += value
            elif operation == 1:
                user_cash.balance -= value
            user_cash.save()

            UserCashRecord.objects.create(user_cash=user_cash, value=value, current_balance=user_cash.balance,
                                          operation=operation, notes=notes, ip=ip)

            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail_and_send_email(e)
            return 99900, dict_err.get(99900)

    def get_record_by_user_id(self, user_id):
        return UserCashRecord.objects.select_related("user_cash").filter(user_cash__user_id=user_id)

    def search_records_for_admin(self, nick):
        objs = UserCashRecord.objects.select_related('user_cash').all()

        if nick:
            user = UserBase().get_user_by_nick(nick)
            if user:
                objs = objs.filter(user_cash__user_id=user.id)
            else:
                objs = []
        return objs


class CarWashCashBase(object):

    def get_car_wash_cash_by_car_wash_id(self, car_wash_id, auto_create_obj=False):
        try:
            return CarWashCash.objects.get(car_wash_id=car_wash_id)
        except CarWashCash.DoesNotExist:
            if not auto_create_obj:
                return utils.DictLikeObject(car_wash_id=car_wash_id, balance=Decimal("0.00"))
            else:
                return CarWashCash.objects.create(car_wash_id=car_wash_id)


class CarWashCashRecordBase(object):

    def validate_record_info(self, value, operation, notes):
        value = int(value)
        operation = int(operation)
        assert operation in (0, 1)
        assert value > 0 and notes

    @transaction.commit_manually(using=DEFAULT_DB)
    def add_record_with_transaction(self, car_wash, value, operation, notes, ip=None):
        try:
            errcode, errmsg = self.add_record(car_wash, value, operation, notes, ip)
            if errcode == 0:
                transaction.commit(using=DEFAULT_DB)
            else:
                transaction.rollback(using=DEFAULT_DB)
            return errcode, errmsg
        except Exception, e:
            debug.get_debug_detail(e)
            transaction.rollback(using=DEFAULT_DB)
            return 99900, dict_err.get(99900)

    @car_wash_required
    def add_record(self, car_wash, value, operation, notes, ip=None):
        """
        @note: 流水记录
        """
        try:
            try:
                value = Decimal(value)
                operation = int(operation)
                self.validate_record_info(value, operation, notes)
            except Exception, e:
                return 99801, dict_err.get(99801)

            car_wash_cash = CarWashCashBase().get_car_wash_cash_by_car_wash_id(car_wash.id, auto_create_obj=True)

            if operation == 1 and car_wash_cash.balance - value < 0:
                return 30100, dict_err.get(30100)

            if operation == 0:
                car_wash_cash.balance += value
            elif operation == 1:
                car_wash_cash.balance -= value
            car_wash_cash.save()

            CarWashCashRecord.objects.create(car_wash_cash=car_wash_cash, value=value, current_balance=car_wash_cash.balance,
                                             operation=operation, notes=notes, ip=ip)

            return 0, dict_err.get(0)
        except Exception, e:
            debug.get_debug_detail(e)
            return 99900, dict_err.get(99900)
