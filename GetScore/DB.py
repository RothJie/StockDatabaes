import pymysql


class DB:  # "stock_history_data" "myfirstdb"
    user, pwd, port, database = "root", "abc123", 3306, "stock_history_data"

    @classmethod
    def setInfo(cls, user_: str, pwd_: str, port_: int, database_: str):
        cls.user = user_
        cls.pwd = pwd_
        cls.port = port_
        cls.database = database_

    @classmethod
    def getInfo(cls):
        return cls.user, cls.pwd, cls.port, cls.database

    @classmethod
    def buildConnection(cls, connection: pymysql.Connect = None):
        if connection is None:
            info = cls.getInfo()
            connection = pymysql.Connect(user=info[0], password=info[1], port=info[2], database=info[3])
            return connection
        else:
            connection.commit()
            connection.close()

    @classmethod
    def executeUniSQL(cls, sql: str = "show tables;"):
        if ";" not in sql:
            sql += ";"
        connection = cls.buildConnection()
        cursor = connection.cursor()
        cursor.execute(sql)
        data_ = [uni[0] for uni in cursor.fetchall()]
        cursor.close()
        cls.buildConnection(connection)
        return data_

    @classmethod
    def executeManySQL_getDta(cls, sql_s: list):
        connection = cls.buildConnection()
        cursor = connection.cursor()
        datas_ = []
        for sql in sql_s:
            if ";" not in sql:
                sql += ";"

            cursor.execute(sql)
            data_ = [list(uni) for uni in cursor.fetchall()]
            datas_.append(data_)
        cursor.close()
        cls.buildConnection(connection)
        return datas_


if __name__ == '__main__':
    print(DB.executeUniSQL("show tables"))
