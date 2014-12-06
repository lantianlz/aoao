# -*- coding: utf-8 -*-

import time
import requests
import json
import logging
from django.conf import settings
from pyquery import PyQuery as pq

from common import cache, debug
from www.misc import consts


dict_err = {
    70100: u'暂无绑定的设备，请取消关注公众号后重新扫描二维码',
}
dict_err.update(consts.G_DICT_ERROR)


weixin_api_url = 'https://api.weixin.qq.com'
dict_weixin_app = {
    'aoaoxc_test': {'app_id': 'wx0d227d4f9b19658a', 'app_secret': '513bdaf5b6022df4913f4cb5543fa688', 'app_type': 'gh_65671b9fff9d',
                    'token': 'aoaoxc_test', 'url': ''},
    'aoaoxc': {'app_id': 'wx23cca542b396c669', 'app_secret': 'dd8cc9591fa32514eed8876e652e6260', 'app_type': 'gh_de7e674b94d4',
               'token': 'aoaoxc', 'url': ''},
}


class WexinBase(object):

    def __init__(self):
        self.cache = cache.Cache()

    def __del__(self):
        del self.cache

    def init_app_key(self, default_value="aoaoxc"):
        return "aoaoxc_test" if settings.LOCAL_FLAG else default_value

    def get_base_text_response(self):
        '''
        @note: 文字信息模板
        '''
        return u'''
        <xml>
        <ToUserName><![CDATA[%(to_user)s]]></ToUserName>
        <FromUserName><![CDATA[%(from_user)s]]></FromUserName>
        <CreateTime>%(timestamp)s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%(content)s]]></Content>
        </xml>
        '''

    def get_base_news_response(self, items=None):
        '''
        @note: 图文信息模板
        '''
        return u'''
        <xml>
        <ToUserName><![CDATA[%(to_user)s]]></ToUserName>
        <FromUserName><![CDATA[%(from_user)s]]></FromUserName>
        <CreateTime>%(timestamp)s</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>%(articles_count)s</ArticleCount>
        <Articles>
        ''' + (items or self.get_base_news_item_response()) + \
            '''
        </Articles>
        </xml>
        '''

    def get_base_news_item_response(self):
        return u'''
        <item>
        <Title><![CDATA[%(title)s]]></Title> 
        <Description><![CDATA[%(des)s]]></Description>
        <PicUrl><![CDATA[%(picurl)s]]></PicUrl>
        <Url><![CDATA[%(hrefurl)s]]></Url>
        </item>
        '''

    def get_base_content_response(self, to_user, from_user, content):
        base_xml = self.get_base_text_response()
        return base_xml % dict(to_user=from_user, from_user=to_user, timestamp=int(time.time()), content=content)

    def get_error_response(self, to_user, from_user, error_info):
        base_xml = self.get_base_text_response()
        return base_xml % dict(to_user=from_user, from_user=to_user, timestamp=int(time.time()), content=error_info)

    def get_subscribe_event_response(self, to_user, from_user):
        content = (u'我们已经恭候您多时了！洗车的时候能想到嗷嗷，人家真是幸福呢...\n'
                   u'嗷嗷洗车是专属于年轻人的洗车平台，这里有更优惠的价格，更贴心的服务，更丰富的活动——洗车用嗷嗷，就对了！'
                   )
        return self.get_base_content_response(to_user, from_user, content=content)

    def get_customer_service_response(self, to_user, from_user):
        return u'''
        <xml>
        <ToUserName><![CDATA[%(to_user)s]]></ToUserName>
        <FromUserName><![CDATA[%(from_user)s]]></FromUserName>
        <CreateTime>%(timestamp)s</CreateTime>
        <MsgType><![CDATA[transfer_customer_service]]></MsgType>
        </xml>
        ''' % dict(to_user=from_user, from_user=to_user, timestamp=int(time.time()))

    def format_input_xml(self, xml):
        '''
        @note: 标签替换为小写，以便pyquery能识别
        '''
        for key in ['ToUserName>', 'FromUserName>', 'CreateTime>', 'MsgType>', 'Content>', 'MsgId>', 'PicUrl>',
                    'MediaId>', 'Format>', 'ThumbMediaId>', 'Event>', 'EventKey>', 'Ticket>', 'Recognition>',
                    'DeviceID>', 'SessionID>', 'DeviceType>', 'OpenID>']:
            xml = xml.replace(key, key.lower())
        return xml

    def get_response(self, xml):
        from www.account.interface import UserBase

        xml = self.format_input_xml(xml)
        jq = pq(xml)
        to_user = jq('tousername')[0].text
        from_user = jq('fromusername')[0].text
        events = jq('event')
        app_key = self.get_app_key_by_app_type(to_user)
        logging.error(u'收到一个来自app：%s 的请求' % app_key)

        # 事件
        if events:
            event = events[0].text.lower()
            if event in ('scan', 'subscribe'):  # 扫码登陆事件
                tickets = jq('ticket')
                if tickets:
                    ticket = tickets[0].text
                    errcode, errmsg = UserBase().login_by_weixin_qr_code(ticket, from_user, app_key)
                    return self.get_base_content_response(to_user, from_user, errmsg)
            if event in ('subscribe',):
                return self.get_subscribe_event_response(to_user, from_user)
            elif event in ('click', ):
                event_key = jq('eventkey')[0].text.lower()
                if event_key == 'hotest':
                    pass

        # 文字识别
        msg_types = jq('msgtype')
        if msg_types:
            msg_type = msg_types[0].text
            if msg_type == 'text':
                content = jq('content')[0].text.strip()
                logging.error(u'收到用户发送的文本数据，内容如下：%s' % content)
                return self.get_customer_service_response(to_user, from_user)   # 多客服接管

    def get_app_key_by_app_type(self, app_type):
        for key in dict_weixin_app:
            if dict_weixin_app[key]['app_type'] == app_type:
                return key
        raise Exception, u'app_key not found by: %s' % app_type

    def send_msg_to_weixin(self, content, to_user, app_key, msg_type='text', img_info=''):
        '''
        @note: 发送信息给微信
        '''
        # json的dumps字符串中中文微信不识别，修改为直接构造
        if msg_type == 'text':
            data = u'{"text": {"content": "%s"}, "msgtype": "%s", "touser": "%s"}' % (content, msg_type, to_user)
        else:
            data = u'{"news":{"articles": %s}, "msgtype":"%s", "touser": "%s"}' % (img_info, msg_type, to_user)

        data = data.encode('utf8')

        access_token = self.get_weixin_access_token(app_key)
        url = '%s/cgi-bin/message/custom/send?access_token=%s' % (weixin_api_url, access_token)
        r = requests.post(url, data=data, timeout=30, verify=False)
        r.raise_for_status()
        content = json.loads(r.content)
        logging.error('send msg to weixin resp is %s' % (content,))

    def get_weixin_access_token(self, app_key):
        # 本地调试模式不走缓存
        if not settings.LOCAL_FLAG:
            key = 'weixin_access_token_for_%s' % app_key
            access_token = self.cache.get(key)
            if access_token is None:
                access_token, expires_in = self.get_weixin_access_token_directly(app_key)
                if access_token:
                    self.cache.set(key, access_token, int(expires_in))
        else:
            access_token, expires_in = self.get_weixin_access_token_directly(app_key)
        return access_token

    def get_weixin_access_token_directly(self, app_key):
        access_token, expires_in = '', 0
        content = ''
        url = '%s/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (weixin_api_url, dict_weixin_app[app_key]['app_id'],
                                                                                    dict_weixin_app[app_key]['app_secret'])
        try:
            r = requests.get(url, timeout=20, verify=False)
            content = r.content
            r.raise_for_status()
            content = json.loads(content)
            access_token = content['access_token']
            expires_in = content['expires_in']
        except Exception, e:
            logging.error(u'get_weixin_access_token rep is %s' % content)
            debug.get_debug_detail(e)
        assert access_token
        return access_token, expires_in

    def get_user_info(self, app_key, openid):
        """
        @note: 获取一关注公众号的用户信息
        """
        access_token = self.get_weixin_access_token(app_key)
        url = '%s/cgi-bin/user/info?access_token=%s&openid=%s' % (weixin_api_url, access_token, openid)
        data = {}
        try:
            r = requests.get(url, timeout=20, verify=False)
            text = r.text
            r.raise_for_status()
            data = json.loads(text)
            if data.get("errmsg") or data.get("subscribe") == 0:
                logging.error("error user info data is:%s" % data)
                data = {}
        except Exception, e:
            debug.get_debug_detail(e)
        return data

    def get_qr_code_ticket(self, app_key, expire=300):
        """
        @note: 获取二维码对应的ticket
        """
        access_token = self.get_weixin_access_token(app_key)
        url = '%s/cgi-bin/qrcode/create?access_token=%s' % (weixin_api_url, access_token)
        data = u'{"expire_seconds":%s, "action_name":"QR_SCENE", "action_info": {"scene": {"scene_id": %s}}' % (expire, int(time.time() * 1000))
        data = data.encode('utf8')

        result = {}
        try:
            r = requests.post(url, data=data, timeout=20, verify=False)
            text = r.text
            r.raise_for_status()
            result = json.loads(text)
            if result.get("errmsg") or result.get("subscribe") == 0:
                logging.error("error create_qr_code result is:%s" % result)
                result = {}
        except Exception, e:
            debug.get_debug_detail(e)
        return result
