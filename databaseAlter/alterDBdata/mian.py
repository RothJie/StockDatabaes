from ConnectMySQL import *

info = ("root", "abc123", "localhost", 3306, "new_stocks")
pool = Pool()
pool.setInfo(*info)
Execute.pool = pool


# tableNames = Execute.uni_sql_val("show tables;")
# for tableName in tableNames:
#     print(tableName)

# s3170
# stock_names
# stock_namesInfo = Execute.uni_sql_val("desc stock_names;")
# for uni_info in stock_namesInfo:
#     print(uni_info)

# 假设现在有一个表需要复制，请生成对应的SQL语句？
def copyTableStructure(table: str):
    table_structureInfo = Execute.uni_sql_val("desc {};".format(table))
    sql = f"create table {table} ("
    for i in range(len(table_structureInfo)):
        uni_info = table_structureInfo[i]
        if i == len(table_structureInfo) - 1:
            sql += f"{uni_info[0]} {uni_info[1]});\n"
            break
        sql += f"{uni_info[0]} {uni_info[1]},"
    return sql


def copyTableRecords(table: str):
    table_records = Execute.uni_sql_val("select * from {};".format(table))
    sql_li = []
    for record in table_records:  # ('20230620', '12.72', '13.5', '12.41', '13.34', '12.6', '0.74', '5.87', '174831', '229718405.0')
        sql = f"insert into {table} values" + str(record) + ";\n"
        sql_li.append(sql)
    return sql_li


# 这里的最后一项必须是一个你的现有数据库
'''
复制整个数据库
1.生成创建数据库的SQL语句
    create database if not exists new_stocks character set 'utf-8';
2.变更正在使用的数据库
    use new_stocks;
3.创建表
    3.1 读取表的结构  -----> 生成创建表的SQL语句
    3.2 读取表的记录  -----> 生成插入表记录的SQL语句
4.执行所有的SQL语句即可完成数据库和表的复制
'''

if __name__ == '__main__':
    path = str(input("请选择数据库保存的文件夹地址可以是U盘:"))
    tableNames = Execute.uni_sql_val("show tables;")
    with open(file=path+"/database.sql", mode="a", encoding="utf-8") as f:
        f.write("create database if not exists new_stocks character set 'utf-8';\n")
        f.flush()
        f.write("use new_stocks;\n")
        f.flush()
        for tableName in tableNames:
            f.write(copyTableStructure(tableName[0]))
            for uni_record in copyTableRecords(tableName[0]):
                f.write(uni_record)
                f.flush()
            f.flush()
            break


