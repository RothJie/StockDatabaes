import json
import requests
import re


def get_industry(stock_code_):
    def judge(stock_code: str):
        if (stock_code[0] == "0") or (stock_code[0] == "3"):
            return "sz" + stock_code
        if stock_code[0] == "6":
            if stock_code[1] == "8":
                return "kcb/" + stock_code
            else:
                return "sh" + stock_code
        if (stock_code[0] == "4") or stock_code[0] == "8":
            return "bj/" + stock_code

    url = f"http://quote.eastmoney.com/{judge(stock_code=str(stock_code_))}.html"
    print(url)

    headers = {
        "Cookie": "qgqp_b_id=990173e8eabf3230b343c6ba48acebba; st_si=99325721640194; st_asi=delete; HAList=ty-0-300991-%u521B%u76CA%u901A%2Cty-0-300605-%u6052%u950B%u4FE1%u606F%2Cty-0-300010-%u8C46%u795E%u6559%u80B2%2Cty-0-873527-%u591C%u5149%u660E; st_pvi=87972847446323; st_sp=2022-12-18%2023%3A14%3A53; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=9; st_psi=20221219202712377-113200301201-9182964752",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    response = requests.get(url=url, headers=headers)
    pattern = re.compile('var quotedata = (.*?);')
    pattern1 = re.compile('<span class="quote_title_name quote_title_name_190" title=".*?">(?P<name>.*?)</span>')
    gs = pattern1.findall(response.text)
    result_ = re.search(pattern, response.text)
    if result_ is None:
        return "暂无行业"
    else:
        result = json.loads(result_.groups()[0])
        return result['bk_name'], gs[0]


if __name__ == '__main__':
    print(get_industry("000541"))

