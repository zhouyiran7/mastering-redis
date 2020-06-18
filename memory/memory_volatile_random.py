import redis
import uuid

local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)


class ValatileLRU():
    def __init__(self):
        local_redis.flushdb()
        local_redis.config_set("maxmemory-policy", "volatile-random")
        print(local_redis.info("memory"))

    def add_id_expire(self, redis_instance):
        count = redis_instance.incr("global:uuid")
        redis_key = "uuid:{}".format(count)
        redis_instance.set(redis_key, str(uuid.uuid4))
        if count % 2 == 0:
            redis_instance.expire(redis_key, 300)


def main():
    policy = ValatileLRU()

    while 1:
        policy.add_id_expire(local_redis)


if __name__ == '__main__':
    main()
