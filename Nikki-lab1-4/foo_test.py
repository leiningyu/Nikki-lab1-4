import pytest
from hypothesis import given, strategies as st
from foo import HashSet  # 替换为实际模块名

# ---------------------- 基础功能测试 ----------------------
def test_add():
    s = HashSet()
    s.add(1)
    assert s.size() == 1
    s.add(1)  # 重复元素
    assert s.size() == 1
    s.add(None)
    assert s.size() == 2

def test_set():
    s = HashSet()
    s.add(1)
    s.set(1, 2)
    assert s.member(2)
    assert not s.member(1)
    assert s.size() == 1

def test_remove():
    s = HashSet()
    s.add(1)
    assert s.remove(1) is True
    assert s.size() == 0
    assert s.remove(999) is False  # 不存在的元素
    s.add(None)
    assert s.remove(None) is True

def test_size():
    s = HashSet()
    assert s.size() == 0
    s.add(1)
    assert s.size() == 1
    s.add(2)
    assert s.size() == 2

def test_member():
    s = HashSet()
    s.add(1)
    assert s.member(1) is True
    assert s.member(2) is False
    s.add(None)
    assert s.member(None) is True

def test_reverse():
    # 测试单个桶的反转
    s = HashSet(capacity=1)  # 强制所有元素进同一个桶
    s.from_list([1, 2, 3])
    s.reverse()
    assert s.to_list() == [3, 2, 1]  # 现在可以正确断言
    
    # 测试多桶情况
    s = HashSet(capacity=3)
    s.from_list([0, 1, 2, 3])
    s.reverse()
    assert s.to_list() == [2, 1, 3, 0]

# ---------------------- 转换测试 ----------------------
def test_from_list_to_list():
    test_data = [
        [],
        [1],
        [1, 2, 3],
        [None, "a", 3.14]
    ]
    for data in test_data:
        s = HashSet()
        s.from_list(data)
        # 注意集合的无序性
        assert sorted(s.to_list(), key=hash) == sorted(list(set(data)), key=hash)

# ---------------------- 高阶函数测试 ----------------------
def test_filter():
    s = HashSet()
    s.from_list([1, 2, 3, 4])
    filtered = s.filter(lambda x: x % 2 == 0)
    assert sorted(filtered.to_list()) == [2, 4]

def test_map():
    s = HashSet()
    s.from_list([1, 2, 3])
    mapped = s.map(lambda x: x * 2)
    assert sorted(mapped.to_list()) == [2, 4, 6]

def test_reduce():
    s = HashSet()
    assert s.reduce(lambda a,b: a+b, 0) == 0  # 空集合
    
    s.from_list([1,2,3])
    assert s.reduce(lambda a,b: a+b) == 6  # 无初始值
    assert s.reduce(lambda a,b: a+b, 10) == 16  # 有初始值

# ---------------------- 迭代器测试 ----------------------
def test_iterator():
    data = [1, 2, 3]
    s = HashSet()
    s.from_list(data)
    collected = []
    for x in s:
        collected.append(x)
    assert sorted(collected) == sorted(data)
    
    empty_iter = iter(HashSet())
    with pytest.raises(StopIteration):
        next(empty_iter)

# ---------------------- Monoid测试 ----------------------
def test_empty():
    empty = HashSet.empty()
    assert empty.size() == 0
    assert empty.to_list() == []

def test_concat():
    s1 = HashSet().from_list([1, 2])
    s2 = HashSet().from_list([2, 3])
    combined = s1.concat(s2)
    assert sorted(combined.to_list()) == [1, 2, 3]
    
    # 空集合测试
    empty = HashSet.empty()
    combined = empty.concat(s1)
    assert combined.to_list() == s1.to_list()

# # ---------------------- 基于属性的测试 ----------------------
# @given(st.lists(st.one_of(st.integers(), st.text(), st.none())))
# def test_from_to_list_equivalence(data):
#     s = HashSet()
#     s.from_list(data)
#     # 考虑集合特性和哈希顺序
#     assert set(s.to_list()) == set(data)
#     assert len(s.to_list()) == len(set(data))

# @given(st.lists(st.integers()))
# def test_size_equivalence(data):
#     s = HashSet()
#     s.from_list(data)
#     assert s.size() == len(set(data))

# @given(st.integers(), st.integers())
# def test_monoid_laws():
#     # 准备测试数据
#     a = 1
#     b = 2
    
#     # 单位元测试
#     empty = HashSet.empty()
#     s = HashSet().from_list([a])
#     assert s.concat(empty).to_list() == s.to_list()
#     assert empty.concat(s).to_list() == s.to_list()
    
#     # 结合律测试
#     s1 = HashSet().from_list([a])
#     s2 = HashSet().from_list([b])
#     s3 = s1.concat(s2)
#     assert sorted(s3.to_list()) == [1, 2]
    
#     # None处理测试
#     s_none = HashSet().from_list([None])
#     combined = s_none.concat(empty)
#     assert None in combined.to_list()

# # ---------------------- 边界测试 ----------------------
# def test_none_handling():
#     s = HashSet()
#     s.add(None)
#     assert s.size() == 1
#     assert s.member(None) is True
#     s.remove(None)
#     assert s.size() == 0

# def test_collision_handling():
#     # 强制哈希冲突（假设容量为1）
#     s = HashSet(1)
#     s.add(1)
#     s.add("1")
#     assert s.size() == 2
#     assert s.member(1) and s.member("1")

# def test_reduce_exception():
#     s = HashSet()
#     with pytest.raises(TypeError):
#         s.reduce(lambda a,b: a+b)  # 空集合无初始值