# -*- coding: utf-8 -*-
import datetime

from django.db import models


class Company(models.Model):

    name = models.CharField(max_length=32, unique=True)
    car_wash_count = models.IntegerField(default=0)  # 旗下洗车行数量


class CarWash(models.Model):

    """
    @note: 洗车行
    """
    wash_type_choices = ((0, u'人工'), (1, u'机器'), (2, u''), )

    company = models.ForeignKey("Company", null=True)   # 洗车行对应的集团公司
    city_id = models.IntegerField(db_index=True)
    district_id = models.IntegerField(db_index=True)

    name = models.CharField(max_length=64, unique=True)
    business_hours = models.CharField(max_length=64)  # 营业时间
    tel = models.CharField(max_length=32)
    addr = models.CharField(max_length=256)
    longitude = models.CharField(max_length=32, null=True)  # 经度
    latitude = models.CharField(max_length=32, null=True)  # 纬度
    wash_type = models.IntegerField(default=0, db_index=True, choices=wash_type_choices)    # 洗车方式
    des = models.TextField(null=True)  # 简介
    note = models.TextField(null=True)   # 温馨提示，使用提醒
    rating = models.IntegerField(default=0, db_index=True)  # 评分
    lowest_sale_price = models.FloatField(db_index=True)  # 最低售价
    lowest_origin_price = models.FloatField()  # 最低原价
    order_count = models.IntegerField(default=0, db_index=True)  # 订单数量
    imgs = models.TextField()  # 多张轮播图融为一个字段

    valid_date_start = models.DateTimeField(null=True)  # 有效期开始时间
    valid_date_end = models.DateTimeField(null=True)  # 有效期结束时间
    is_vip = models.BooleanField(default=False)
    vip_info = models.CharField(max_length=64, null=True)

    sort_num = models.IntegerField(default=0, db_index=True)
    state = models.BooleanField(default=True, db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s, %s' % (self.id, self.name)


class CarWashBank(models.Model):

    """
    @note: 洗车行结算信息
    """
    car_wash = models.ForeignKey("CarWash")
    manager_name = models.CharField(max_length=16)
    mobile = models.CharField(max_length=16)
    tel = models.CharField(max_length=16)
    bank_name = models.CharField(max_length=16)
    bank_card = models.CharField(max_length=32)
    balance_date = models.DateField(null=True)  # 结算日期


class ServiceType(models.Model):

    """
    @note: 服务类型
    """
    name = models.CharField(max_length=32, unique=True)
    group = models.IntegerField(default=0, db_index=True)  # 大类
    sort_num = models.IntegerField(default=0, db_index=True)
    state = models.BooleanField(default=True, db_index=True)


class ServicePrice(models.Model):

    """
    @note: 服务价格
    """
    car_wash = models.ForeignKey("CarWash")
    service_type = models.ForeignKey("ServiceType")

    sale_price = models.FloatField(db_index=True)  # 售价
    origin_price = models.FloatField(db_index=True)  # 原价
    clear_price = models.FloatField(db_index=True)  # 和厂商结算价
    sort_num = models.IntegerField(default=0, db_index=True)
    state = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["sort_num", "sale_price"]
        unique_together = [("car_wash", "service_type"), ]

"""
订单
优惠码
"""
