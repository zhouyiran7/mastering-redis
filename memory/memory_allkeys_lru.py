#LRU 驱逐策略
# 持久化部分 redis 键(例如配置或引用查找), 不使用 allkeys-lru 策略

import redis
import uuid

local_datastore = redis.StrictRedis(host='localhost', port=6379, db=0)


#allkeys-lru: 驱逐所有LRU 算法下的键
class ValatileLRU():
    def __init__(self):
        local_datastore.flushdb()
        # 设置内存驱逐策略 valatile-lru
        local_datastore.config_set("maxmemory-policy", "allkeys-lru")
        print(local_datastore.info("memory"))

    def add_id(self, redis_instance):
        redis_key = "uuid:{}".format(redis_instance.incr("global:uuid"))
        redis_instance.set(redis_key, str(uuid.uuid4))


def main():
    policy = ValatileLRU()
    while 1:
        policy.add_id(local_datastore)


if __name__ == '__main__':
    main()
