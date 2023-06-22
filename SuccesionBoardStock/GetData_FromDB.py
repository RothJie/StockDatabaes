import time

from databaseAlter.ConnectMySQL import useWay


def judge(uin_fu: float):
    if (uin_fu > float(9.90)) and (uin_fu < float(11)):
        return True
    else:
        return False


def getBoard(data: list):
    j = 0
    for t in data:
        if t == '-':
            break
        if judge(float(t)):
            j += 1
        else:
            break
    return j


infoDict = dict()


def getInfo(table_name: str):
    data_ = [[s[0], s[1]] for s in useWay(f'select 涨跌幅,股票名称 from {table_name} limit 15')]
    name_ = data_[0][1]
    data_1 = [u[0] for u in data_]
    board = getBoard(data_1)
    if board > 0:
        if f"{board}board" not in infoDict:
            infoDict[f"{board}board"] = []
            infoDict[f"{board}board"].append((name_, table_name.strip("csv").zfill(6)))
        else:
            infoDict[f"{board}board"].append((name_, table_name.strip("csv").zfill(6)))


n = 100
allPart = [u[0] for u in useWay("show tables;")]
uniParts = [allPart[i: n+i] for i in range(0, len(allPart), n)]
for i in range(len(uniParts)):
    print(f"正在进行 {i+1} 部分的数据处理......")
    for uni_name in uniParts[i]:
        getInfo(uni_name)
    time.sleep(3)


infoDictKey = sorted(infoDict, reverse=True)

stringInfo = ""
for key in infoDictKey:
    stringInfo += key + ":"
    for (name, code) in infoDict[key]:
        stringInfo += str(name)
        stringInfo += str(code).zfill(6) + " "
    stringInfo += "\n"

with open(file="./上板日志.txt", mode="w", encoding="utf8") as f:
    f.write(stringInfo)
# 从这里开始运行
