import pytest
from hypothesis import given, strategies as st
from sc import HashSet

def test_add():
    s = HashSet()
    s.add(1)
    assert s.size() == 1
    s.add(1)  # Repeat elements
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
    assert s.remove(999) is False  # Non-existent elements
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
    # Test a single bucket inversion
    s = HashSet(capacity=1)  # Force all elements into the same bucket
    s.from_list([1, 2, 3])
    s.reverse()
    assert s.to_list() == [3, 2, 1]
    
    # Test multiple bucket conditions
    s = HashSet(capacity=3)
    s.from_list([0, 1, 2, 3])
    s.reverse()
    assert s.to_list() == [2, 1, 3, 0]

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
        # Notice the disorder of the set
        assert sorted(s.to_list(), key=hash) == sorted(list(set(data)), key=hash)

def test_filter():
    s = HashSet()
    s.from_list([1, 2, 3, 4])
    filtered = s.filter(lambda x: x % 2 == 0)
    assert sorted(filtered.to_list()) == [2, 4]

    s = HashSet()
    s.from_list([1, None, 3, 4])
    filtered = s.filter(lambda x: x is not None)
    assert sorted(filtered.to_list()) == [1, 3, 4]

def test_map():
    s = HashSet()
    s.from_list([1, 2, 3])
    mapped = s.map(lambda x: x * 2)
    assert sorted(mapped.to_list()) == [2, 4, 6]

    s = HashSet()
    s.from_list([1, None, 3])
    mapped = s.map(lambda x: 0 if x is None else x)
    assert sorted(mapped.to_list(), key=lambda x: str(x)) == [0, 1, 3]


def test_reduce():
    s = HashSet()
    assert s.reduce(lambda a,b: a+b, 0) == 0  # Empty set
    
    s.from_list([1,2,3])
    assert s.reduce(lambda a,b: a+b) == 6  # No initial value
    assert s.reduce(lambda a,b: a+b, 10) == 16

    s = HashSet()
    s.from_list([1, None, 3])
    # view None as 0
    result = s.reduce(lambda a, b: a + (b if b is not None else 0), 0)
    assert result == 4

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

# Monoid test
def test_empty():
    empty = HashSet.empty()
    assert empty.size() == 0
    assert empty.to_list() == []

def test_concat():
    s1 = HashSet().from_list([1, 2])
    s2 = HashSet().from_list([2, 3])
    combined = s1.concat(s2)
    assert sorted(combined.to_list()) == [1, 2, 3]

    s1 = HashSet().from_list([1, None])
    s2 = HashSet().from_list([None, 3])
    combined = s1.concat(s2)
    assert sorted(combined.to_list(), key=lambda x: str(x)) == [1, 3, None]
    
    # Empty set test
    empty = HashSet.empty()
    combined = empty.concat(s1)
    assert combined.to_list() == s1.to_list()
