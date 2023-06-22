import pymysql


class ConnectMysql(object):
    def __init__(self):
        self.__name = "root"
        self.__Port = 3306
        self.__Host = "localhost"  # ip地址会变化
        self.__pwd = "abc123"
        self.__database = "stock_history_data"
        self.flag = False

    def connectMethod(self, conn_=None):
        if self.flag:
            conn_ = pymysql.connect(host=self.__Host, password=self.__pwd, user=self.__name, port=self.__Port,
                                    database=self.__database)
            return conn_
        else:
            conn_.commit()
            conn_.close()


def useWay(sql: str):
    Cm = ConnectMysql()  # 创建对象
    Cm.flag = True
    conn_ = Cm.connectMethod()

    cursor = conn_.cursor()
    cursor.execute(sql + ";")
    data = cursor.fetchall()
    Cm.flag = False
    Cm.connectMethod(conn_)
    return data


# def useWay1(sqls: list):
#     Cm = ConnectMysql()  # 创建对象
#     Cm.flag = True
#     conn_ = Cm.connectMethod()
#
#     cursor = conn_.cursor()
#     cursor.execute(sql + ";")
#     data = cursor.fetchall()
#     Cm.flag = False
#     Cm.connectMethod(conn_)
#     return data

if __name__ == '__main__':
    # print(useWay('show tables'))
    print([[s[0], s[1]] for s in useWay('select 涨跌幅,股票名称 from 600519csv limit 15')])
