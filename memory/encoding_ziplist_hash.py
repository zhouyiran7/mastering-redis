import matplotlib.pyplot as plt
import redis


"""
通过设置hash-max-ziplist-entries(默认 512)和hash-max-ziplist-valu(默认 64)
ziplist编码在标准哈希表编码下的序列化下的长度的影响
"""
local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)


def size(instance: redis.StrictRedis, key: str):
    debug = instance.debug_object(key)
    return debug.get("serializedlength")


def reset(instance: redis.StrictRedis):
    instance.flushall()


# 通过不同的hash-max-ziplist-entries设置, 查看标准哈希表编码的序列化长度
def plot_hashes(runs=500, zip_list_entries=512) -> slice:
    # 重置数据库
    reset(local_redis)

    key = "test-hash"

    ser_ist = []
    local_redis.config_set("hash-max-ziplist-entries", zip_list_entries)
    for i in range(runs):
        field = "f{}".format(i)
        local_redis.hset(key, field, i)
        list.append(size(local_redis, key))

    print(local_redis.debug_object(key).get("serializedlength"))

    return ser_ist


# 比对不同hash-max-ziplist-entries设置下的哈希表的序列化长度变化
l1 = plot_hashes(500, 512)  # 3102
l2 = plot_hashes(500, 0)  # 3764

zip_list, hash_map = plt.plot(l1, 'r--', l2, 'g-')
plt.title("Redis Hash Encodings Ziplist vs. Hashtable")
plt.xlabel("Number of Fields in Hash")
plt.ylabel("Size of Hash in Bytes")
plt.legend((zip_list, hash_map), ('ziplist', 'hash-table'), loc='lower right')
plt.show()
