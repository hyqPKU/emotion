# coding=utf-8

import hashlib
import time
import random
import string
import urllib
import sys

import requests
from bs4 import BeautifulSoup
import json

reload(sys)
sys.setdefaultencoding('utf-8')

def get_params(text):
    """请求时间戳（秒级），用于防止请求重放（保证签名5分钟有效）"""
    t = time.time()
    time_stamp = int(t)

    # 请求随机字符串，用于保证签名不可预测
    nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))

    # 应用标志
    app_id = '1106888447'
    app_key = 'mQVqxCTW4rD8p5pk'

    # 值使用URL编码，URL编码算法用大写字母
    text1 = text
    text = urllib.quote(text1.decode(sys.stdin.encoding).encode('utf8')).upper()

    # 拼接应用密钥，得到字符串S
    sign_before = 'app_id=' + app_id + '&nonce_str=' + nonce_str + '&text=' + text + '&time_stamp=' + str(
        time_stamp) + '&app_key=' + app_key

    # 计算MD5摘要，得到签名字符串
    m = hashlib.md5()
    m.update(sign_before)
    sign = m.hexdigest()
    sign = sign.upper()

    params = 'app_id=' + app_id + '&time_stamp=' + str(
        time_stamp) + '&nonce_str=' + nonce_str + '&sign=' + sign + '&text=' + text

    return params


def get_content(text):
    url = "https://api.ai.qq.com/fcgi-bin/nlp/nlp_textpolar"  # API地址
    params = get_params(text)  # 获取请求参数
    url = url + '?' + params  # 请求地址拼接
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        allcontents = soup.select('body')[0].text.strip()
        allcontents_json = json.loads(allcontents)  # str转成dict

        return allcontents_json["data"]["polar"], allcontents_json["data"]["confd"]
    except Exception, e:
        print('error calling TOP', str(e))
        return 0, 0
