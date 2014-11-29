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
    from www.weixin.interface import WexinBase
    wb = WexinBase()
    app_key = "aoao_test"
    to_user = 'o07dat0ujliP84s4GPsLFXOrAcbk'
    content = (u'古人云：鸟随鸾凤飞腾远，人伴贤良品质高。\n')

    # print wb.send_msg_to_weixin(content, to_user, app_key)
    # print wb.get_weixin_access_token(app_key="aoao_test")

    from www.tasks import async_send_email_worker
    async_send_email_worker.delay('lantian-lz@163.com', title="来自嗷嗷洗车", content="邮件发送")

    from common.utils import replace_href_to_open_blank
    body = """
    <p>目前市场上用的最多的炒股软件有三款：大智慧，通达信，同花顺。大部分证券公司也提供这三款软件的定制版，都是可以免费使用的。</p><p><br></p>
    """
    # print replace_href_to_open_blank(body)

if __name__ == '__main__':
    main()
