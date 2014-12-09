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
