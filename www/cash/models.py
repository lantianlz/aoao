# -*- coding: utf-8 -*-

from django.db import models


class UserCash(models.Model):

    """
    @note: 用户现金账户
    """
    user_id = models.CharField(max_length=32, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0, db_index=True)


class CarWashCash(models.Model):

    """
    @note: 洗车行现金账户
    """
    car_wash_id = models.IntegerField(unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0, db_index=True)


operation_choices = ((0, u"转入"), (1, u"转出"))


class UserCashRecord(models.Model):

    """
    @note: 用户现金账户流水
    """

    user_cash = models.ForeignKey(UserCash)
    value = models.DecimalField(max_digits=20, decimal_places=2, db_index=True)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2, db_index=True)
    operation = models.IntegerField(choices=operation_choices, db_index=True)  # 转入or转出
    notes = models.CharField(max_length=256)    # 流水介绍
    ip = models.CharField(max_length=32, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)  # 创建时间

    class Meta:
        ordering = ['-id']


class CarWashCashRecord(models.Model):

    """
    @note: 洗车现金账户流水
    """
    car_wash_cash = models.ForeignKey(CarWashCash)
    value = models.DecimalField(max_digits=20, decimal_places=2, db_index=True)
    current_balance = models.DecimalField(max_digits=20, decimal_places=2, db_index=True)
    operation = models.IntegerField(choices=operation_choices, db_index=True)  # 转入or转出
    notes = models.CharField(max_length=256)    # 流水介绍
    ip = models.CharField(max_length=32, null=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)  # 创建时间

    class Meta:
        ordering = ['-id']


class CashOrder(models.Model):

    """
    @note: 充值订单
    """
    pay_type_choices = ((0, u'零支付'), (1, u'支付宝'), (2, u'微信'))
    order_state_choices = ((0, u'未付款'), (1, u'已付款'), )

    trade_id = models.CharField(max_length=32, db_index=True, unique=True)  # 非自增id,可以修改
    user_id = models.CharField(max_length=32, db_index=True)

    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 总的结算金额
    discount_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 优惠金额
    pay_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 应付金额   最终需要用户支付金额
    pay_type = models.IntegerField(default=0, choices=pay_type_choices, db_index=True)  # 支付方式

    payed_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # 支付接口回调反馈的实际付款金额
    pay_time = models.DateTimeField(null=True, blank=True)  # 支付接口回调的时间
    pay_info = models.CharField(max_length=256, null=True, blank=True)  # 用户支付成功后保存支付信息
    order_state = models.IntegerField(default=0, choices=order_state_choices, db_index=True)  # 订单状态,默认为未确认状态
    is_admin_modify_pay_fee = models.BooleanField(default=False)  # 管理员是否修改应付金额
    ip = models.IPAddressField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-id', ]
