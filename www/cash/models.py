# -*- coding: utf-8 -*-

from django.db import models


class UserCash(models.Model):

    """
    @note: 用户现金账户
    """


class CarWashCash(models.Model):

    """
    @note: 洗车行现金账户
    """


class UserTransaction(models.Model):

    """
    @note: 用户现金账户流水
    """


class CarWashTransaction(models.Model):

    """
    @note: 洗车现金账户流水
    """
