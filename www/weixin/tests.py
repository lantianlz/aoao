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
    from django.conf import settings
    from common import utils
    from www.weixin.interface import WexinBase
    from www.tasks import async_send_email

    wb = WexinBase()
    app_key = "aoao_test"
    to_user = 'o07dat0ujliP84s4GPsLFXOrAcbk'
    content = (u'古人云：鸟随鸾凤飞腾远，人伴贤良品质高。\n')

    # print wb.send_msg_to_weixin(content, to_user, app_key)
    # print wb.get_weixin_access_token(app_key="aoao_test")

    context = {'reset_url': '%s/reset_password?code=%s' % (settings.MAIN_DOMAIN, "123"), }
    async_send_email("web@aoaoxc.com", u'来自嗷嗷洗车', utils.render_email_template('email/reset_password.html', context), 'html')


if __name__ == '__main__':
    main()
