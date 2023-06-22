import json
import requests
import re
from ConnectMySQL import *
from downloadDayData import *

# 建立连接池
pool = Pool()
info = ("root", "abc123", "localhost", 3306, "new_stocks")
pool.setInfo(*info)
Execute.pool = pool


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
        return [gs[0], "暂无行业"]
    else:
        result = json.loads(result_.groups()[0])
        return [gs[0], result['bk_name']]


def get_info_fromWeb(code: str):
    if len(code) != 6:
        code = str(code).zfill(6)
    # 数据库中没有的表，怎么办？ ----》创建表
    # 1.需要在 stock_names 中注册该表的信息，对应的 编号,股票代码,股票名称,所属行业
    # 2.获取编号
    # 2.1 获取 stock_names 表中的 最大编号
    id_max = Execute.uni_sql_val("SELECT 编号 FROM stock_names ORDER BY 编号 DESC LIMIT 0,1;")[0][0]
    # 2.2 在 最大编号 的基础上 加一个 ---------> 新表的 编号
    id_max = int(str(id_max).lstrip("s")) + 1

    # 3.根据股票代码----> 解析出 股票名称 和
    info_register = [id_max, code] + get_industry(code)
    return [
        f"CREATE TABLE IF NOT EXISTS s{id_max}(交易日期 varchar(30),开盘 varchar(30),最高 varchar(30),最低 varchar(30),收盘 varchar(30),前收盘 varchar(30),涨跌额 varchar(30),涨跌幅 varchar(30),成交量 varchar(30),成交额 varchar(30));",
        f"INSERT INTO stock_names VALUES('{info_register[0]}', '{info_register[1]}', '{info_register[2]}', '{info_register[3]}');"]


"""
交易日期 varchar(30),开盘 varchar(30),最高 varchar(30),最低 varchar(30),收盘 varchar(30),前收盘 varchar(30),涨跌额 varchar(30),涨跌幅 varchar(30),成交量 varchar(30),成交额 varchar(30) 
"""


def insertDayDataToDB():
    with open(file="./codes.json", mode="r", encoding="utf-8") as f1:
        codes = json.load(f1)
        id_stocks = {uni[1]: uni[0] for uni in Execute.uni_sql_val("select * from stock_names;")}
        not_haveInDB = [uni for uni in codes if uni not in id_stocks]  # 正常情况下需要将数据库中没有该表的的表创建出来
        print("数据库中没有的表:", not_haveInDB)
        sql_li = []
        for uni in not_haveInDB:
            sql_li += get_info_fromWeb(uni)
        print("正在创建数据库中没有的表....")
        Execute.many_sql(sql_li)

    with open(file="./dataInterface.json", mode="r", encoding="utf-8") as f2:
        dict_all_stock_info = json.load(f2)
        id_stocks = {uni[1]: uni[0] for uni in Execute.uni_sql_val("select * from stock_names;")}
        sql_li_ = []
        for key in dict_all_stock_info:
            uni_info = dict_all_stock_info[key]
            sql = f"insert into {id_stocks[key]} values('{uni_info[0]}','{uni_info[1]}','{uni_info[2]}','{uni_info[3]}','{uni_info[4]}','{uni_info[5]}','{uni_info[6]}','{uni_info[7]}','{uni_info[8]}','{uni_info[9]}');"
            print(sql)
            sql_li_.append(sql)
        Execute.many_sql(sql_li_)
        print("所有数据添加完成。")


if __name__ == '__main__':
    print("正在下载数据....")
    download()
    print("数据已经写入完毕...")
    insertDayDataToDB()