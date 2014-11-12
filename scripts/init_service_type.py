# -*- coding: utf-8 -*-


import sys
import os

# 引入父目录来引入其他模块
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'


def main():
    from www.car_wash.interface import ServiceTypeBase
    datas = [u"标准洗车(5座)", u"标准洗车(7座)", u"精致洗车(5座)", u"精致洗车(7座)"]
    for data in datas:
        ServiceTypeBase().add_service_type(data)
    print 'ok'


if __name__ == '__main__':
    main()
