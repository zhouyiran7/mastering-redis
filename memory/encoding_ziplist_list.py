import redis
import matplotlib.pyplot as plt
import uuid

"""
ziplist 编码用于小型列表, 阈值由list-max-ziplist-entries 和 list-max-ziplist-value 决定
默认值分别是 512 和 64
"""

local_redis = redis.StrictRedis(host='localhost', port=6379, db=0)


def size(instance: redis.StrictRedis, key: str):
    debug = instance.debug_object(key)
    return debug.get("serializedlength")


def reset(instance: redis.StrictRedis):
    instance.flushall()


def plot_list(runs=500, zip_list_entries=512) -> slice:
    reset(local_redis)

    key = "test-list"
    ser_list = []
    run = []

    local_redis.config_set('hash-max-ziplist-entries', zip_list_entries)
    for i in range(runs):
        run.append(i)
        local_redis.lpush(key, str(uuid.uuid4()))
        ser_list.append(size(local_redis, key))

    print(local_redis.debug_object(key).get("serializedlength"))
    return ser_list


# 比对不同hash-max-ziplist-entries设置下的哈希表的序列化长度变化

runs = 600
zip_list = plot_list(runs, 512)
linked_list = plot_list(runs, 0)
l1, l2 = plt.plot(zip_list, 'r--', linked_list, 'g-')
title = "Redis List Encoding "
if runs < 100:
    title += "Very Small Lists"
else:
    title += "Ziplist vs. Linked List"
plt.title(title)
plt.xlabel("Number of UUIDs")
plt.ylabel("Serialized Lengths in Bytes")
plt.legend((l1, l2), ('ziplist', 'linked-list'), loc='lower right')
plt.show()
