# -*- coding: utf-8 -*-


import sys
import os

# 引入父目录来引入其他模块
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'


def update_user_avatar():
    import urllib2
    import logging
    from django.conf import settings

    from www.misc import qiniu_client
    from www.weixin.interface import WexinBase
    from www.account.models import Profile, ExternalToken
    from www.account.interface import UserBase

    for i, user in enumerate(Profile.objects.filter(avatar="")):
        print i
        openid = ExternalToken.objects.get(user_id=user.id, source="weixin").external_user_id

        weixin_user_info = WexinBase().get_user_info(WexinBase().init_app_key(), openid)
        if weixin_user_info:

            weixin_img_url = weixin_user_info.get("headimgurl")
            user_avatar = ''
            if weixin_img_url:
                # 上传图片

                flag, img_name = qiniu_client.upload_img(urllib2.urlopen(weixin_img_url, timeout=20), img_type='weixin_avatar')
                if flag:
                    user_avatar = '%s/%s' % (settings.IMG0_DOMAIN, img_name)
                else:
                    logging.error(u'转换微信图片失败，weixin_img_url is %s' % weixin_img_url)

            user.avatar = user_avatar
            user.save()

            # 更新缓存
            UserBase().get_user_by_id(user.id, must_update_cache=True)

    print 'ok'


if __name__ == '__main__':
    update_user_avatar()
