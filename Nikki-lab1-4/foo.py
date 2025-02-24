from functools import reduce

class HashSet:
    DEFAULT_CAPACITY = 16

    def __init__(self, capacity=DEFAULT_CAPACITY):
        self.capacity = max(1, capacity)
        self.buckets = [[] for _ in range(self.capacity)]
        self._size = 0

    def _hash(self, value):
        return hash(value) % self.capacity if value is not None else 0

    # 1. Add a new element
    def add(self, value):
        idx = self._hash(value)
        if value not in self.buckets[idx]:
            self.buckets[idx].append(value)
            self._size += 1

    # 2.  Set an element with a specific  index/key
    def set(self, old_value, new_value):
        if self.member(old_value):
            self.remove(old_value)
            self.add(new_value)

    # 3. Remove an element
    def remove(self, value):
        idx = self._hash(value)
        try:
            self.buckets[idx].remove(value)
            self._size -= 1
            return True
        except ValueError:
            return False

    # 4. Size
    def size(self):
        return self._size

    # 5. Is a member
    def member(self, value):
        return value in self.buckets[self._hash(value)]

    # 6. Reverse
    def reverse(self):
        for bucket in self.buckets:
            bucket.reverse()   
        self.buckets.reverse()

    # 7. From built-in list
    def from_list(self, lst):
        for item in lst:
            self.add(item)
        return self


    # 8. To built-in list
    def to_list(self):
        return [item for bucket in self.buckets for item in bucket]

    # 9. Filter data structure by a specific predicate
    def filter(self, predicate):
        new_set = HashSet(self.capacity)
        for bucket in self.buckets:
            for item in bucket:
                if predicate(item):
                    new_set.add(item)
        return new_set

    # 10. Map
    def map(self, f):
        new_set = HashSet(self.capacity)
        for bucket in self.buckets:
            for item in bucket:
                new_set.add(f(item))
        return new_set

    # 11. Reduce process elements and build a value by the function
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

    # 12. Data structure should be an iterator
    def __iter__(self):
        for bucket in self.buckets:
            yield from bucket

    def __next__(self):
        return next(iter(self))

    # 13. Monoid
    @classmethod
    def empty(cls):
        return cls(1)  # Minimum capacity

    # 14. Concat
    def concat(self, other):
        new_set = HashSet()
        if self:  # empty set
            new_set.from_list(self.to_list())
        if other:
            new_set.from_list(other.to_list())
        return new_set
