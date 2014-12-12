# -*- coding: utf-8 -*-


import os
import sys

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
# 引入父目录来引入其他模块
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'


import requests

from pprint import pprint
from pyquery import PyQuery as pq
from django.utils.encoding import smart_str
from common.hashcompat import md5_constructor as md5

from common.weixinpay.config_real import settings
from common import debug, utils


MAIN_DOMAIN = 'http://www.aoaoxc.com'
WEIXINPAY_URL = 'https://api.mch.weixin.qq.com'


class Weixinpay(object):

    def __init__(self):
        self.appid = settings.APPID
        self.mch_id = settings.MCH_ID
        self.sign_key = settings.SIGN_KEY
        self.input_charset = "utf8"

    def format_params(self, params):
        ks = params.keys()
        ks.sort()
        newparams = {}
        prestr = ''
        for k in ks:
            v = params[k]
            k = smart_str(k, self.input_charset)
            newparams[k] = smart_str(v, self.input_charset)
            if k not in ('sign', 'sign_type') and v != '':
                prestr += '%s=%s&' % (k, newparams[k])
        prestr = prestr[:-1]
        return newparams, prestr

    def build_mysign(self, prestr):
        """
        @note: md5签名, 转成大写
        """
        return md5("%s&key=%s" % (prestr, self.sign_key)).hexdigest().upper()

    def get_prepay_id(self, body, out_trade_no, total_fee, openid, attach="", trade_type="JSAPI", ip="121.42.48.184", notify_url=None):
        """
        @note: total_fee单位为分，不能带小数点
        """
        url = "%s/pay/unifiedorder" % WEIXINPAY_URL
        notify_url = notify_url or ("%s/weixinnotify" % MAIN_DOMAIN)

        params = dict(appid=self.appid, mch_id=self.mch_id,
                      nonce_str=utils.uuid_without_dash(), body=body, attach=attach,
                      out_trade_no=out_trade_no, total_fee=total_fee, spbill_create_ip=ip,
                      notify_url=notify_url, trade_type=trade_type, openid=openid)

        params, prestr = self.format_params(params)
        sign = self.build_mysign(prestr)
        params["sign"] = sign

        xml = """
        <xml>
        <appid>%(appid)s</appid>
        <attach><![CDATA[%(attach)s]]></attach>
        <body><![CDATA[%(body)s]]></body>
        <mch_id>%(mch_id)s</mch_id>
        <nonce_str>%(nonce_str)s</nonce_str>
        <notify_url>%(notify_url)s</notify_url>
        <out_trade_no>%(out_trade_no)s</out_trade_no>
        <spbill_create_ip>%(spbill_create_ip)s</spbill_create_ip>
        <total_fee>%(total_fee)s</total_fee>
        <trade_type>%(trade_type)s</trade_type>
        <openid><![CDATA[%(openid)s]]></openid>
        <sign><![CDATA[%(sign)s]]></sign>
        </xml>
        """ % params

        try:
            # resp = requests.post(url=url, data=xml, timeout=30)
            # resp.encoding = "utf-8"
            # text = resp.text
            text = """
            <xml>
            <return_code><![CDATA[SUCCESS]]></return_code>
            <return_msg><![CDATA[OK]]></return_msg>
            <appid><![CDATA[wx2421b1c4370ec43b]]></appid>
            <mch_id><![CDATA[10000100]]></mch_id>
            <device_info><![CDATA[1000]]></device_info>
            <nonce_str><![CDATA[FvYSnPuFFPkAr77M]]></nonce_str>
            <sign><![CDATA[63238039D6E43634297CF2A6EB5F3B72]]></sign>
            <result_code><![CDATA[SUCCESS]]></result_code>
            <openid><![CDATA[oUpF8uN95-Ptaags6E_roPHg7AG0]]></openid>
            <is_subscribe><![CDATA[Y]]></is_subscribe>
            <trade_type><![CDATA[JSAPI]]></trade_type>
            <bank_type><![CDATA[CCB_CREDIT]]></bank_type>
            <total_fee>1</total_fee>
            <coupon_fee>0</coupon_fee>
            <fee_type><![CDATA[CNY]]></fee_type>
            <transaction_id><![CDATA[1008450740201407220000058756]]></transaction_id>
            <out_trade_no><![CDATA[1406033828]]></out_trade_no>
            <prepay_id><![CDATA[123456]]></prepay_id>
            <time_end><![CDATA[20140722160655]]></time_end>
            </xml>
            """
            text = smart_str(text)
            if "prepay_id" in text:
                jq = pq(text)
                prepay_id = jq('prepay_id').html()
                self.prepay_id = prepay_id

                return True, prepay_id
            else:
                return False, text
        except Exception, e:
            debug.get_debug_detail_and_send_email(e)
            return False, e


if __name__ == '__main__':
    weixinpay = Weixinpay()
    weixinpay.get_prepay_id(body=u"嗷嗷洗车", out_trade_no="W2014120815441258305", total_fee=2000, openid="oNYsJj1eg4fnU4tKLvH")
