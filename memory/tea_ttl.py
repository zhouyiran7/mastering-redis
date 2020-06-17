import redis

tea_datastore = redis.StrictRedis(host='localhost', port=6379, db=0)

TEA_BREW_FISHED = "fished"
TEA_BREW_BREWING = "brewing"


# 键过期示例 ttl
class Tea():
    def __init__(self):
        tea_datastore.flushdb()

    def create_tea(self, datastore, name, time, size):
        # Increment and save global counter
        tea_counter = datastore.incr("global:teas")
        tea_key = "tea:{}".format(tea_counter)
        datastore.hmset(
            tea_key,
            {
                # 名称
                "name": name,
                # 冲沏时间
                "brew-time": time,
                # 茶盒大小
                "box-size": size,
            })
        return tea_key

    def add_box_of_tea(self, datastore, tea_key, number):
        box_counter = datastore.incr("global:{}:boxes".format(tea_key))
        tea_box_key = "{}:box:{}".format(tea_key, box_counter)
        datastore.sadd(tea_box_key, *range(1, number + 1))
        return tea_box_key

    # 开始沏茶
    def start_brew(self, datastore, tea_box_key):
        tea_box = tea_box_key.split(":box")[0]
        expire_time = int(datastore.hget(tea_box, "brew-time")) * 60
        tea_bag_number = datastore.spop(tea_box_key)
        tea_bag_key = "{}:bag:{}".format(tea_box_key, tea_bag_number.decode())
        datastore.set(tea_bag_key, "brew")
        datastore.expire(tea_bag_key, expire_time)
        datastore.sadd("brewing", tea_bag_key)

    # 遍历正在沏茶的茶袋,通过 ttl 查询每个茶袋的剩余时间
    def poll_brewing(self, datastore):
        active_tea_bags = datastore.smembers("brewing")

        tea_len = len(active_tea_bags)
        brew_fished_count = 0
        for tea_bag in active_tea_bags:
            time_left = datastore.ttl(tea_bag)
            if time_left > 0:
                print("{} seconds left for {}".format(time_left, tea_bag))
            else:
                print("{} Ready to Drink!".format(tea_bag))
                datastore.srem("brewing", tea_bag)
                brew_fished_count = brew_fished_count + 1

        if brew_fished_count == tea_len:
            return TEA_BREW_FISHED

        return TEA_BREW_BREWING


def main():
    t = Tea()

    # 创建三类茶并存储为 Hash
    earl_grey = t.create_tea(tea_datastore, "Earl Grey", 5, 15)
    lavender_mint = t.create_tea(tea_datastore, "Lavender Mint", 2, 20)
    peppermint_puch = t.create_tea(tea_datastore, "Peppermint Punch", 4, 10)

    # 每种类型的茶袋添加到各自的第一个茶盒中
    earl_grey_box_1 = t.add_box_of_tea(tea_datastore, earl_grey, 15)
    print(tea_datastore.smembers(earl_grey_box_1))

    lavender_mint_box_1 = t.add_box_of_tea(tea_datastore, lavender_mint, 15)
    print(tea_datastore.scard(lavender_mint_box_1))

    peppermint_puch_box_1 = t.add_box_of_tea(tea_datastore, peppermint_puch,
                                             10)
    print(tea_datastore.scard(peppermint_puch_box_1))

    tea_boxes = [earl_grey_box_1, lavender_mint_box_1, peppermint_puch_box_1]

    # 为每种茶沏茶
    for tea_box_key in tea_boxes:
        t.start_brew(tea_datastore, tea_box_key)

    # 查询茶袋剩余时间
    isFished = TEA_BREW_BREWING
    while isFished == TEA_BREW_BREWING:
        isFished = t.poll_brewing(tea_datastore)


if __name__ == '__main__':
    main()
