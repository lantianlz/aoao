# -*- coding: utf-8 -*-

import os
import sys

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
# 引入父目录来引入其他模块
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

import random
import datetime
from common import utils
from www.cash import interface

ucrb = interface.UserCashRecordBase()
cwcrb = interface.CarWashCashRecordBase()

user_id = "d081652b603211e48a41685b35d0bf16"


def main():
    datas = [
        (100, 0, u"在线充值", "112.112.11.1"),
        # (20, 1, u"购买洗车码", None),
    ]

    for data in datas:
        value, operation, notes, ip = data
        errcode, errmsg = ucrb.add_record(user_id, value, operation, notes, ip)
        if errcode:
            print errmsg.encode("utf8")
        # print cwcrb.add_record(1, value, operation, notes, ip)


if __name__ == '__main__':
    main()
