
# Redis内部编码说明

## 哈希

- ziplist（压缩列表): 元素个数小于**hash-max-ziplist-entries**（默认512个）且同时所有值都小于**hash-max-ziplist-value**（默认64字节）

- hashtable（哈希表): 无法满足ziplist的条件时

## 列表

### redis v3.2版本之前

- ziplist(压缩列表) 同上
- linkedlist(链表)

### redis 3.2版本之后

- quicklist

## 集合

- intset(整数集合): 集合中的元素都是整数且元素个数小于set-max-intset-entries（默认512个）
- hashtable(哈希表)

## 有序集合

- ziplist(压缩列表): 当元素个数小于zset-max-ziplist-entries（默认128个），同时每个元素的值都小于zset-max-ziplist-value（默认64字节）时
- skiplist(跳跃表)
