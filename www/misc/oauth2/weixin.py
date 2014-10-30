# -*- coding: utf-8 -*-

'''
@author: lizheng
@date: 2014-01-01
'''
import requests
import urllib
import re
import json
from pprint import pprint

from django.conf import settings
import logging

CLIENT_ID = 'wx0d227d4f9b19658a'
CLIENT_SECRET = '513bdaf5b6022df4913f4cb5543fa688'
API_URL = 'https://api.weixin.qq.com'
REDIRECT_URI = '%s/account/oauth/weixin' % (settings.MAIN_DOMAIN if settings.LOCAL_FLAG == False else "http://192.168.0.103:8002")


class Consumer(object):

    def __init__(self, response_type='code'):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.api_url = API_URL
        self.response_type = response_type
        self.redirect_uri = urllib.quote_plus(REDIRECT_URI)
        self.state = 'aoaoxc_state'
        self.grant_type = 'authorization_code'
        self.dict_format = dict(appid=self.client_id, client_secret=self.client_secret,
                                response_type=self.response_type, api_url=self.api_url, grant_type=self.grant_type,
                                redirect_uri=self.redirect_uri, state=self.state)

    def authorize(self):
        return ('https://open.weixin.qq.com/connect/oauth2/authorize?appid=%(appid)s'
                '&redirect_uri=%(redirect_uri)s&response_type=%(response_type)s&scope=snsapi_base&state=%(state)s#wechat_redirect') % self.dict_format

    def token(self, code):
        self.dict_format.update(dict(code=code))

        access_token_url = ('%(api_url)s/sns/oauth2/access_token?grant_type=%(grant_type)s&'
                            'appid=%(appid)s&secret=%(client_secret)s&code=%(code)s') % self.dict_format

        rep = requests.get(access_token_url, timeout=30)
        content = rep.text
        dict_result = json.loads(content)
        return dict_result

    def refresh_token(self, refresh_token):
        pass

    def request_api(self, access_token, method_name, data={}, method='GET'):
        request_url = '%(api_url)s%(method_name)s' % dict(api_url=self.api_url, method_name=method_name)
        data.update(oauth_consumer_key=self.client_id)
        if method == 'GET':
            request_url = '%s?%s' % (request_url, urllib.urlencode(data))
            rep = requests.get(request_url, timeout=30)
        else:
            rep = requests.post(request_url, data=data, timeout=30)
        content = rep.content
        try:
            return json.loads(content)
        except:
            return content

    def get_openid(self, access_token):
        pass