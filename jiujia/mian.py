import json
import urllib3
import hashlib
import requests
import time

md5 = hashlib.md5()
urllib3.disable_warnings()

request = requests.Session()  # 实例化requests.Session对象
base_url = "https://cloud.cn2030.com"  # URL变量
proxies = {'https': '127.0.0.1:8888', 'http': '127.0.0.1:8888'}  # 测试代{过}{滤}理

# 待自动化
session = '抓包补充'

user_info = '{"status":200,"user":{"birthday":"1998-06-10","tel":"17879525579","cname":"陈行","sex":1,"idcard":"362201199806102252","doctype":1}}'

hpv_id = '1'

with open("hospital.json", encoding='UTF-8') as f:
    result = json.load(f)

hospital_list = result['list']


# 请求头获取Zftsl字段
def getZftsl():
    str_time = str(round(time.time() * 100))
    str1 = "zfsw_" + str_time
    md5.update(str1.encode("utf-8"))
    value = md5.hexdigest()
    return value


for item in hospital_list:
    get_product_url = 'https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx?act=CustomerProduct&id={}&lat={}&lng={}'.format(
        item['id'], item['lat'], item['lng'])
    headers = {
        'Host': 'cloud.cn2030.com',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001433) NetType/WIFI Language/zh_CN',
        'content-type': 'application/json;UTF-8',
        'zftsl': getZftsl(),
        'Referer': 'https://servicewechat.com/wx2c7f0f3c30d99445/97/page-frame.html',
        'Accept-Encoding': 'gzip,deflate, br'
    }
    resp = request.get(url=get_product_url, headers=headers, )
    if resp.status_code == 200:
        hospital = resp.json()
        if hospital['status'] == 200:
            for hpv in hospital['list']:
                if hpv['text'] == '九价人乳头瘤病毒疫苗' and not hpv['enable']:
                    print(hpv)

