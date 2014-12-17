# -*- coding: utf-8 -*-

import logging
import datetime
from decimal import Decimal
from django.db import transaction

from common import utils, debug
from www.misc import consts
from www.account.interface import UserBase
from www.car_wash.interface import car_wash_required, CarWashBase
from www.cash.models import UserCash, UserCashRecord, CarWashCash, CarWashCashRecord, CashOrder

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

    def get_records_by_user_id(self, user_id):
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

    def get_records_by_car_wash_id(self, car_wash_id):
        return CarWashCashRecord.objects.select_related("car_wash_cash").filter(car_wash_cash__car_wash_id=car_wash_id)

    def get_records_by_range_date(self, car_wash_id, start_date, end_date, operation=None):
        ps = dict(car_wash_cash__car_wash_id=car_wash_id, create_time__gt=start_date, create_time__lt=end_date)
        if operation is not None:
            ps.update(dict(operation=operation))
        return CarWashCashRecord.objects.select_related("car_wash_cash").filter(**ps)

    def format_records_with_day(self, records):
        """
        @note: 将流水按天汇总
        """
        dict_results = {}
        for record in records:
            day = str(record.create_time.date())
            value = float(record.value)
            if day not in dict_results:
                dict_results[day] = value
            else:
                dict_results[day] += value
        return dict_results

    def search_records_for_admin(self, car_wash_name):
        objs = CarWashCashRecord.objects.select_related('car_wash_cash').all()

        if car_wash_name:
            car_wash = CarWashBase().get_car_washs_by_name(car_wash_name, None)
            if car_wash:
                objs = objs.filter(car_wash_cash__car_wash_id=car_wash[0].id)
            else:
                objs = []
        return objs


class CashOrderBase(object):

    def validate_order_info(self, user_id, pay_type, total_fee):
        assert user_id and pay_type
        assert 1000 > total_fee > 0
        assert pay_type in (1, 2)

    def create_order(self, user_id, pay_type, total_fee, ip=None):
        try:
            from www.car_wash.interface import OrderBase

            try:
                pay_type = int(pay_type)
                total_fee = float(total_fee)
                self.validate_order_info(user_id, pay_type, total_fee)   # 检测基本信息
            except:
                return 99801, dict_err.get(99801)

            pay_fee = total_fee
            trade_id = OrderBase().generate_order_trade_id(pr="R")

            ps = dict(trade_id=trade_id, user_id=user_id, total_fee=total_fee, discount_fee=0, pay_fee=pay_fee, pay_type=pay_type, ip=ip)
            order = CashOrder.objects.create(**ps)

            return 0, order
        except Exception, e:
            debug.get_debug_detail_and_send_email(e)
            return 99900, dict_err.get(99900)

    def get_order_by_id(self, id, state=None):
        try:
            ps = dict(id=id)
            if state is not None:
                ps.update(state=state)
            return CashOrder.objects.get(**ps)
        except CashOrder.DoesNotExist:
            pass

    def get_order_by_trade_id(self, trade_id, state=None):
        try:
            ps = dict(trade_id=trade_id)
            if state is not None:
                ps.update(state=state)
            return CashOrder.objects.get(**ps)
        except CashOrder.DoesNotExist:
            pass

    @transaction.commit_manually(using=DEFAULT_DB)
    def cash_order_pay_callback(self, trade_id, payed_fee, pay_info='', order=None):
        '''
        @note: 充值回调函数
        '''
        try:
            from www.tasks import async_send_email
            from www.car_wash.interface import dict_err as dict_err_car_wash

            errcode, errmsg = 0, dict_err.get(0)
            payed_fee = float(payed_fee)
            order = order

            if (not order) and trade_id.startswith('R'):
                order = self.get_order_by_trade_id(trade_id)
            if not order:
                transaction.rollback(using=DEFAULT_DB)
                return 20301, dict_err_car_wash.get(20301)

            if order.order_state in (0, ):
                # 付款金额和订单应付金额是否相符
                if abs(payed_fee - float(order.pay_fee)) > Decimal(0.001):
                    errcode, errmsg = 20302, dict_err_car_wash.get(20302)
                order.payed_fee = str(payed_fee)  # 转成string后以便转成decimal
                order.pay_info = pay_info
                order.pay_time = datetime.datetime.now()

                # 增加用户现金账户余额
                if errcode == 0:
                    errcode, errmsg = UserCashRecordBase().add_record(order.user_id, payed_fee, 0, notes=u"%s充值" % order.get_pay_type_display())

                # 发送邮件
                if payed_fee > 0:
                    user = UserBase().get_user_by_id(order.user_id)
                    title = u'诸位，钱来了'
                    if errcode != 0:
                        title += u"(状态异常，订单号:%s, errcode:%s, errmsg:%s)" % (trade_id, errcode, errmsg)
                    content = u'收到用户「%s」通过「%s」的付款 %.2f 元，用于充值' % (user.nick, order.get_pay_type_display(), payed_fee)
                    async_send_email("vip@aoaoxc.com", title, content)

                if errcode == 0:
                    # 保存订单信息
                    order.order_state = 1
                    order.save()
                else:
                    transaction.rollback(using=DEFAULT_DB)
                    return errcode, errmsg

            elif order.order_state < 0:
                errcode, errmsg = 20303, dict_err_car_wash.get(20303)

            transaction.commit(using=DEFAULT_DB)
            return errcode, errmsg
        except Exception, e:
            debug.get_debug_detail_and_send_email(e)
            transaction.rollback(using=DEFAULT_DB)
            return 99900, dict_err.get(99900)
