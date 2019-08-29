# -*- coding: utf-8 -*-
import redis
from random import  choice


users_id = ["001", "002", "003", "004"]


rd = redis.Redis("127.0.0.1")
if not rd.exists("goods_total"):
    rd.set("goods_total", "10")
for a in range(100):
    user_id = choice(users_id)
    have_count = rd.llen("qianggou:2019-8-20")
    print("当前抢购的人数", have_count)
    if have_count >= int(rd.get("goods_total")):
        print("抢光了")
    else:
        result = rd.lpush("qianggou:2019-8-20", user_id)
        if result:
            print("抢成功", user_id)
        else:
            print("抢失败")
