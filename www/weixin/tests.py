# -*- coding: utf-8 -*-

import os
import sys

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
# 引入父目录来引入其他模块
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'


user_id = 'f762a6f5d2b711e39a09685b35d0bf16'


def main():
    import time
    from django.conf import settings
    from common import utils
    from www.weixin.interface import WexinBase
    from www.tasks import async_send_email
    from pprint import pprint

    wb = WexinBase()
    app_key = "aoaoxc_test"
    to_user = 'oZy3hskE524Y2QbLgY2h3VnI3Im8'

    app_key = "aoaoxc"
    to_user = 'oNYsJj1eg4fnU4tKLvH-f2IXlxJ4'
    content = (u'古人云：鸟随鸾凤飞腾远，人伴贤良品质高。\n')

    # print wb.send_msg_to_weixin(content, to_user, app_key)
    # print wb.get_weixin_access_token(app_key="aoao_test")

    context = {'reset_url': '%s/reset_password?code=%s' % (settings.MAIN_DOMAIN, "123"), }
    # async_send_email("web@aoaoxc.com", u'来自嗷嗷洗车', utils.render_email_template('email/reset_password.html', context), 'html')

    # pprint(wb.get_user_info(app_key, to_user))
    # pprint(wb.get_qr_code_ticket(app_key))
    pprint(wb.send_template_msg(app_key, to_user))


if __name__ == '__main__':
    main()
