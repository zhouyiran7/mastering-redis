import uuid
import redis

local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)


# 默认淘汰策略, 不驱逐数据
class NoevictionPolicy():
    def __init__(self):
        local_redis.set("maxmemory", "1mb")

    # CONFIG GET maxmemory-policy
    # maxmemory-policy
    # noeviction (默认策略, 当没有可用内存时, 如果 redis 尝试写入数据库就会返回错误)
    def add_id(self, redis_instance):
        redis_key = "uuid:{}".format(redis_instance.incr("global:uuid"))
        redis_instance.set(redis_key, str(uuid.uuid4))


while 1:
    # redis 内存数据达到maxmemory,报错
    NoevictionPolicy().add_id(local_redis)
    # redis.exceptions.ResponseError: OOM command not allowed when used memory > 'maxmemory'.
