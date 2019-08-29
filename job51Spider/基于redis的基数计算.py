# -*- coding: utf-8 -*-

import redis
rd = redis.Redis()

# rd.pfadd("rename", [1])
rd.pfadd("rename1", [1, 4, 1,  5])
no_repeat_count = rd.pfcount("rename1")
print(no_repeat_count)
