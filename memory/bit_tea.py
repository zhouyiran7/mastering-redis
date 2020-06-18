import redis
import random

"""
位图优化内存
通过集合和位图序列化后的数据比对, 发现位图比集合更加节省内存.
但稀疏位图会有空间浪费的情况,比如: 每个偏移量的首个位置被设置,而其余的位都未被使用
"""
INSTANCE1 = redis.StrictRedis()


def populate_tea(full=True):
    for i in range(10000):
        if random.random() <= .6:
            member = i
            if full:
                member = "tea:{}".format(i)
            INSTANCE1.sadd("teas:caffeinated", member)
            INSTANCE1.setbit("teas:caffeine", i, 1)


populate_tea()

hash_ser_len = INSTANCE1.debug_object(
    "teas:caffeinated").get("serializedlength")
bit_ser_len = INSTANCE1.debug_object("teas:caffeine").get("serializedlength")

print("Hash Serialized Length | Bit Serialized Length")
print("{} | {}".format(hash_ser_len, bit_ser_len))
