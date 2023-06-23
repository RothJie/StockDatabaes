import csv
import time

from ConnectMySQL import *

sql = """
    SELECT t3.id, t3.code, t3.name, t3.inds, t1.n, t2.l, t2.h,(((t1.n-t2.l)/(t2.h-t2.l))*100) AS score,t1.n_day/t4.avg_vol
    FROM (
        SELECT CONVERT(成交量, DECIMAL(10,3)) n_day, CONVERT(收盘, DECIMAL(10,3)) AS n
        FROM {0} 
        ORDER BY 交易日期 DESC LIMIT 0,1
        ) t1,(
            SELECT MIN(CONVERT(最低, DECIMAL(10,3))) AS l,MAX(CONVERT(最高, DECIMAL(10,3))) AS h
            FROM {0} 
            WHERE (最高 != "-") AND (最低 != "-") AND (收盘 != "-")
            ORDER BY 交易日期 DESC LIMIT 100
            ) t2,(
                SELECT 编号 AS id,股票代码 AS `code`, 股票名称 AS `name`,所属行业 AS inds  
                FROM stock_names WHERE 编号='{0}'		
                ) t3, (
                    SELECT AVG(n_day) avg_vol
                    FROM (
                        SELECT CONVERT(成交量, DECIMAL(10,3)) AS n_day
                        FROM {0} 
                        WHERE (最高 != "-") AND (最低 != "-") AND (收盘 != "-")
                        ORDER BY 交易日期 DESC LIMIT 0,7
                        ) deal_num
                    ) t4;
""".format

pool = Pool()
info = ("root", "abc123", "localhost", 3306, "new_stocks")
pool.setInfo(*info)
Execute.pool = pool
tab = Execute.uni_sql_val('show tables')

f = open(file="result.csv", mode="w", encoding="utf-8")
k = 0
for e_tab in tab:
    if e_tab[0] == "stock_names":
        continue
    data = Execute.uni_sql_val(sql=sql(e_tab[0]))
    d = [str(u) if ((type(u) == str) or (u is None)) else str(float(u)) for u in data[0]]
    f.write(",".join(d)+"\n")
    k += 1
    if k % 200 == 0:
        time.sleep(3)
        print(f'已经完成了{k}只')
print(f'共{k}只，已经全部完成。')
f.close()
