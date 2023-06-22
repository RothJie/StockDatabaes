from engine import *
from datetime import datetime


def JudgeCode(code: str):
    code_list = [int(u) for u in list(code.zfill(6))]
    if code_list[0] == 0:
        return True
    elif code_list[0] == 6:
        if code_list[1] == 8:
            return False
        else:
            return True
    else:
        return False


def JudgeName(name: str):
    name_list = list(name)
    if "*" in name_list:
        return False
    elif "S" in name_list:
        return False
    elif "退" in name_list:
        return False
    else:
        return True


def getDate():
    date_today = datetime.today().strftime("%Y%m%d")
    return date_today


def download():
    codes = []
    all_data_dict = {}
    for p in range(1, 265):
        data = get_data(p)
        for idx in range(len(data)):
            code = str(data[idx]["f12"]).zfill(6)
            name = data[idx]["f14"]
            if JudgeCode(code):
                if JudgeName(name):
                    per_ = data[idx]
                    codes.append(code)
                    all_data_dict[code] = [getDate(), per_['f17'], per_['f15'], per_['f16'],
                                           per_['f2'], per_['f18'], per_['f4'], per_['f3'], per_['f5'],
                                           per_['f6']]

    with open(file="./dataInterface.json", mode="w", encoding="utf-8") as fo:
        json.dump(obj=all_data_dict, fp=fo, indent=4, ensure_ascii=False)

    with open(file="./codes.json", mode="w", encoding="utf-8") as fo:
        json.dump(obj=codes, fp=fo, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    download()
