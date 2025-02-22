from functools import reduce

class HashSet:
    DEFAULT_CAPACITY = 16

    def __init__(self, capacity=DEFAULT_CAPACITY):
        self.capacity = max(1, capacity)
        self.buckets = [[] for _ in range(self.capacity)]
        self._size = 0

    def _hash(self, value):
        """处理None值的哈希函数"""
        return hash(value) % self.capacity if value is not None else 0

    # 1. 添加元素
    def add(self, value):
        idx = self._hash(value)
        if value not in self.buckets[idx]:
            self.buckets[idx].append(value)
            self._size += 1

    # 2. 更新元素（集合特性需先删后加）
    def set(self, old_value, new_value):
        if self.member(old_value):
            self.remove(old_value)
            self.add(new_value)

    # 3. 删除元素
    def remove(self, value):
        idx = self._hash(value)
        try:
            self.buckets[idx].remove(value)
            self._size -= 1
            return True
        except ValueError:
            return False

    # 4. 集合大小
    def size(self):
        return self._size

    # 5. 成员判断
    def member(self, value):
        return value in self.buckets[self._hash(value)]

    # 6. 反转所有桶内元素顺序
    def reverse(self):
        for bucket in self.buckets:
            bucket.reverse()   
        self.buckets.reverse()

    # 7. 从列表初始化
    # 修改from_list方法
    def from_list(self, lst):
        for item in lst:
            self.add(item)
        return self  # 添加返回语句


    # 8. 转换为列表
    def to_list(self):
        return [item for bucket in self.buckets for item in bucket]

    # 9. 过滤元素
    def filter(self, predicate):
        new_set = HashSet(self.capacity)
        for bucket in self.buckets:
            for item in bucket:
                if predicate(item):
                    new_set.add(item)
        return new_set

    # 10. 映射函数
    def map(self, f):
        new_set = HashSet(self.capacity)
        for bucket in self.buckets:
            for item in bucket:
                new_set.add(f(item))
        return new_set

    # 11. 归约操作
    def reduce(self, reducer, initial=None):
        it = iter(self)
        if initial is None:
            try:
                value = next(it)
            except StopIteration:
                raise TypeError("Reduce of empty set with no initial value")
        else:
            value = initial
        for element in it:
            value = reducer(value, element)
        return value

    # 12. 迭代器实现
    def __iter__(self):
        for bucket in self.buckets:
            yield from bucket

    def __next__(self):
        return next(iter(self))

    # 13. 单位元（Monoid）
    @classmethod
    def empty(cls):
        return cls(1)  # 最小容量

    # 14. 结合操作（Monoid）
    def concat(self, other):
        new_set = HashSet()
        if self:  # 处理空集合
            new_set.from_list(self.to_list())
        if other:
            new_set.from_list(other.to_list())
        return new_set

    # 特殊方法
    def __str__(self):
        return "{" + ", ".join(map(str, self)) + "}"

    def __contains__(self, value):
        return self.member(value)
