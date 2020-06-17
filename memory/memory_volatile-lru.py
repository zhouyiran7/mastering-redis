import redis

local_datastore = redis.StrictRedis(host='localhost', port=6379, db=0)


class ValatileLRU():
    def __init__(self):
        local_datastore.flushdb()
        # 设置内存驱逐策略 valatile-lru
        local_datastore.config_set("maxmemory-policy", "volatile-lru")
        print(local_datastore.info("memory"))


def main():
    ValatileLRU()


if __name__ == '__main__':
    main()
