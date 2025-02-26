# Nikki - lab 1 - variant 4

A series of functional requirements are realized and tested based on `hash map, separate chaining` method.

## Project structure

- `sc.py` -- implementation of `Set based on hash map, separate chaining` class with `add`, `set`, `remove`, `size`, `member`, `reverse`, `from_list`, `to_list`, `filter`, `map`, `reduce`, `__iter__`, `__next__`, `empty`, `concat` features.
   
- `sc_test.py` -- unit and PBT tests for `sc`.

## Features

- PBT: `test_add`
       `test_set`
       `test_remove`
       `test_size`
       `test_member`
       `test_reverse`
       `test_from_list_to_list`
       `test_filter`
       `test_map`
       `test_reduce`
       `test_iterator`
       `test_empty`
       `test_concat`

## Contribution

- Lei Ningyu (3232254146@qq.com) -- all work.
- Yi Min (1757973489@qq.com) -- all work.

## Changelog

- 22.02.2025 - 0
  - Initial
- 22.02.2025 - 1
  - Update README, sc.py and sc_test.py.
- 24.02.2025 - 2
  - Update README and modify sc.py and sc_test.py.
- 26.02.2025 - 3
  - Update README and modify sc.py and sc_test.py.

## Design notes

- The meaning of hash table split linked list method is to build a linked list with key value pairs for each search array index. Mod a value to find its index, and then put it in the bucket (index), if there is already a duplicate value in the list, do not put.
- When we processed reverse for the first time, the result of test was wrong. Later we found out that we only reversed the order of the elements in the bucket, but in fact we should have reversed the order of the buckets, and the order of the elements in each bucket.
- We tested adding the None value in foo_test.py, and did not find an error. Our implementation works correctly with the None value.
