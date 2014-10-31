# -*- coding: utf-8 -*-
import datetime

from django.db import models


class CarWash(models.Model):
    state_choices = ((0, u''), (1, u''), (2, u''), )

    """
    基本信息：城市、区域、名称、地址、营业时间、电话、经度、纬度、最低原价、最低销售价、机器or人工、有效期开始、有效期截止、介绍、是否加V，加V信息
    冗余字段：订单数、评分数
    银行卡：结算人、手机、固定电话、银行、分行、卡号、结算日

    图片、商品、原价、销售价、结算价
    """

    def __unicode__(self):
        return '%s, %s' % (self.id, self.email)
