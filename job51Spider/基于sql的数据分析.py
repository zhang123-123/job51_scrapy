# -*- coding: utf-8 -*-
import sqlite3
con = sqlite3.connect("job51.sqlite")
cur = con.cursor()

# 统计数据有多少城市
# sql1 = """
#     select job_place from job group by job_place
# """
# cur.execute(sql1)
# result = cur.fetchall()
# print(result)
#
# sql2 = """
#     select count(*) from job
# """
# cur.execute(sql2)
# result = cur.fetchall()
# print(result)
#
# # 统计数据中每个城市有多少工作数量
# sql3 = """
#     select job_place, count(*) from job group by job_place
# """
# cur.execute(sql3)
# result = cur.fetchall()
# print(result)
# # 统计某个城市的工作种类和其对应的数量
# sql4 = """
#     select job_type, count(*) from job where job_place='上海' group by job_type
# """
# cur.execute(sql4)
# result = cur.fetchall()
# print(result)
#
# # 统计上海python每天的岗位数量变化
# sql5 = """
#     select job_time, count(*) from job where job_place='上海' and job_type='python' group by job_time
# """
# cur.execute(sql5)
# result = cur.fetchall()
# print(result)
# 用柱状图表示每个城市每个语言工作数量的对比情况
sql6 = """
    select job_place, count(*) from job group by job_place 
"""

cur.execute(sql6)
result = cur.fetchall()
results = []
for place in result:
    sql7 = f"""
        select job_place, job_type, count(*) from job where job_place='{place[0]}' group by job_type
    """
    cur.execute(sql7)
    result = cur.fetchall()
    results.extend(result)
    # print(result)
print(results)
# results = set(results)
# print(results)
places = []
dict1 = {}
print(type(dict1))
count = []
for a in results:
    if a[0] not in places:
        places.append(a[0])
    if a[1] not in dict1.keys():
        dict1[a[1]] = [a[2]]
    elif dict1[a[1]]:
        dict1[a[1]].append(a[2])
print(places)
print(len(places))
print(dict1)
print(len(dict1["html"]))
# print(count)

from pyecharts import Bar
bar =Bar("我的第一个图表", "这里是副标题")
for key, value in dict1.items():
    if len(value) < len(places):
        for a in range(len(places) - len(value)):
            value.append(None)
    bar.add(key, places, value)
# bar.add("php", ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"], [5, 20, 36, 10, 75, 90])
bar.show_config()
bar.render()
