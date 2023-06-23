import time

import pymysql


class Pool:
    def __init__(self):
        self.__pool = []
        self.__info = ()
        self.set_max_connection_num = 100
        self.__max = 0  # 记录已经在使用的连接的数量
        pass

    def __createConnection(self, n: int = 3):
        for _ in range(n):
            conn = pymysql.Connection(user=self.__info[0], password=self.__info[1], host=self.__info[2],
                                      port=self.__info[3],
                                      database=self.__info[4])
            self.__pool.append(conn)

    def outConn(self, n: int = 3):
        while (self.__max >= self.set_max_connection_num):
            print("已经超过限制的最大连接数...")
            time.sleep(3)
        if len(self.__pool) == 0:
            self.__createConnection(n)
        self.__max += 1
        return self.__pool.pop()

    def putConn(self, conn: pymysql.Connection):
        self.__max -= 1
        self.__pool.append(conn)

    def setInfo(self, user: str, password: str, host: str, port: int, database: str):
        #  ("root", "abc123", "localhost", 3306, "new_stocks")
        self.__info = (user, password, host, port, database)

    def getInfo(self):
        return self.__info

    def connections(self):
        return len(self.__pool)

    def __del__(self):
        for uni_conn in self.__pool:
            uni_conn.close()


class Execute:
    pool: Pool = None

    @classmethod
    def uni_sql(cls, sql: str):
        conn = cls.pool.outConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        cls.pool.putConn(conn)

    @classmethod
    def uni_sql_val(cls, sql: str):
        conn = cls.pool.outConn()
        cursor = conn.cursor()
        cursor.execute(sql)
        val = cursor.fetchall()
        cursor.close()
        conn.commit()
        cls.pool.putConn(conn)
        return val

    @classmethod
    def many_sql(cls, sql_li: list):
        conn = cls.pool.outConn()
        cursor = conn.cursor()
        for sql in sql_li:
            cursor.execute(sql)
        cursor.close()
        conn.commit()
        cls.pool.putConn(conn)

    @classmethod
    def many_sql_val(cls, sql_li: list):
        conn = cls.pool.outConn()
        cursor = conn.cursor()
        data = []
        for sql in sql_li:
            cursor.execute(sql)
            val = cursor.fetchall()
            data.append(val)
        cursor.close()
        conn.commit()
        cls.pool.putConn(conn)
        return data


if __name__ == '__main__':
    pool = Pool()
    info = ("root", "abc123", "localhost", 3306, "new_stocks")
    pool.setInfo(*info)
    Execute.pool = pool
    datas = Execute.uni_sql_val("show tables;")
    for i in datas:
        print(i)
