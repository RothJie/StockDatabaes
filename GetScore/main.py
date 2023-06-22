import json
import time
from DB import DB

print('正在拼接SQL语句。。。。。。。')
fi = open('getSQL.txt', 'r', encoding='utf8').read()
exec(fi)
time.sleep(3)
print('SQL语句拼接完成。。。。。。。。')

print('正在进行全部数据处理，请等待。。。。')


def score(h, low, n):
    h = float(h)
    low = float(low)
    n = float(n)
    if n > h:
        score_ = 0.0
    else:

        score_ = round(((h - n) / (h - low)) * 100, 3)
    return score_


with open(file='sql_s.json', mode='r', encoding="utf8") as f_r:
    sql_li = json.load(f_r)
    all_stock_data = [uni for uni in DB.executeManySQL_getDta(sql_li) if len(uni) >= 30]  # 361 表数据

    resl = []
    for per_stock in all_stock_data:
        h_price_li = []
        l_price_li = []
        volume_li = []
        n_price = float(per_stock[0][5])
        for i in range(len(per_stock)):
            h_price_li.append(float(per_stock[i][3]))
            l_price_li.append(float(per_stock[i][4]))
            if i < 7:
                volume_li.append(float(per_stock[i][6]))
        h_price = max(h_price_li)
        l_price = min(l_price_li)
        sc = score(h_price, l_price, n_price)

        avg_volume = sum(volume_li[1:]) / 5

        use = per_stock[0][0:3]
        use.append(sc)
        use.append(avg_volume)
        use.append(volume_li[0])
        resl.append(use)


print('正在写入数据。。。。。。')
with open(file='OutputScore.csv', encoding='utf8', mode='w') as f:
    f.write("股票代码,股票名称,所属行业,得分,5日均成交量,成交量" + "\n")
    ni = []
    for uni in resl:
        if (uni[3] > 85.0) and (uni[3] < 96.0) and ((uni[-1]/uni[-2]) > 3):
            ni.append(uni[0:3])

        f.write(",".join([str(i) for i in uni])+"\n")

    with open(file="成交量异常放大.txt", mode="w", encoding="utf8") as fi:
        fi.write("股票代码,股票名称,所属行业" + "\n")
        for uni in ni:
            fi.write(",".join([str(i) for i in uni])+"\n")
    print(ni)
print('写入数据完成。。。。。')
