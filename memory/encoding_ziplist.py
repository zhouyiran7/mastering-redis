import redis

local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)


def emptyDB(instance: redis.StrictRedis):
    instance.delete("test-hash")


# 对于哈希表来说, hash-max-ziplist-entries指令设置了总共有多少个字段可以被特殊编码为 ziplist,默认为 512
def dynamic_encoding_switch(instance: redis.StrictRedis):
    emptyDB(instance)
    hash_max_ziplist_entiries = instance.config_get("hash-max-ziplist-entries")
    print(hash_max_ziplist_entiries)

    for i in range(515):
        instance.hset("test-hash", i, 1)

        if i > 510:
            debug = instance.debug_object("test-hash")
            print("Count: {} Length: {} Enconding: {}".format(
                i, debug.get('serializedlength'), debug.get('encoding')))


dynamic_encoding_switch(local_redis)
