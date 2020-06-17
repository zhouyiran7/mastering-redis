import redis
import uuid

local_datastore = redis.StrictRedis(host='localhost', port=6379, db=0)


#volatile-lru:从已设置过期时间的内存数据集中挑选最近最少使用的数据淘汰
class ValatileLRU():
    def __init__(self):
        local_datastore.flushdb()
        # 设置内存驱逐策略 valatile-lru
        local_datastore.config_set("maxmemory-policy", "volatile-lru")
        print(local_datastore.info("memory"))

    def add_id_expire(self, redis_instance):
        count = redis_instance.incr("global:uuid")
        redis_key = "uuid:{}".format(count)
        redis_instance.set(redis_key, str(uuid.uuid4))
        if count <= 75:
            # 策略前提: 设置键的过期时间, 内存满时, 会开始删除过期时间的 key,即使该键仍然未到期
            redis_instance.expire(redis_key, 300)


def main():
    ValatileLRU()


if __name__ == '__main__':
    main()
