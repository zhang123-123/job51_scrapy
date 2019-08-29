# -*- coding: utf-8 -*-

import redis


rd = redis.Redis(
    host="127.0.0.1",
    port="6379",
    db=2  # redis默认16个数据库，编号从0开始
)

# 字符串类型
rd.set("name", "zhangsan")
name = rd.get("name")
print(type(name), name)

# 列表
# lpush = left push = 左侧添加
rd.lpush("stu_name_list", "zhangsan", "lisi", "wangwu")
# rpush = right push = 右侧添加
rd.rpush("stu_name_list", "zhangsan", "lisi", "wangwu")
# rd.lpop()
# rd.rpop()
# stu_name_list = rd.lrange("stu_name_list", 0, 10)
stu_name_list = rd.lrange("stu_name_list", -5, -3)
print(stu_name_list)

# 哈希
rd.hmset("stu_info", {"name": "zhangsan"})
# name = rd.hmget("stu_info", "name")
name = rd.hget("stu_info", "name")
print(name)

