import requests
import re
import json


def setPage(page):
    if 1 <= page <= 264:
        page = page
    else:
        page = 1
        print(f"你输入的page: {page}不对, 页码规范是[1,263)。现在获取的是第1页的数据。")
    return page


def get_data(page):
    url = "http://82.push2.eastmoney.com/api/qt/clist/get"  # 网站地址
    headers = {
        "Cookie": "qgqp_b_id=990173e8eabf3230b343c6ba48acebba; HAList=ty-0-300605-%u6052%u950B%u4FE1%u606F%2Cty-0-300010-%u8C46%u795E%u6559%u80B2%2Cty-0-300991-%u521B%u76CA%u901A%2Cty-0-873527-%u591C%u5149%u660E; st_si=31522563740988; st_asi=delete; st_pvi=87972847446323; st_sp=2022-12-18%2023%3A14%3A53; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=3; st_psi=20221219164730907-113200301321-3389238486",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }

    params = {
        "cb": "jQuery112403101458116538718_1671376614031",
        "pn": f"{setPage(page)}",
        "pz": "20",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "wbp2u": "|0|0|0|web",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "_": "1671376614032"
    }
    response = requests.get(url=url, headers=headers, params=params)  # 请求方式
    print(response.url)
    pattern = re.compile("jQuery112403101458116538718_1671376614031(.*?);")
    result = re.search(pattern, response.text).groups()
    diff_data = json.loads(str(str(result[0]).strip("(")).strip(")"))
    data = diff_data['data']["diff"]
    return data


if __name__ == '__main__':
    dat = get_data(12)
    for u in dat:
        print(u)
