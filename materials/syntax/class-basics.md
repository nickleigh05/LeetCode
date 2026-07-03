# Class Basics

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
p.x       # 3
```

A `class` is a blueprint for objects — it bundles data (attributes) and behavior (methods) together. `self` is the instance itself, always the first parameter of a method, used to access that instance's own attributes. Common in LeetCode for `ListNode`, `TreeNode`, and "design a class" problems (LRU Cache, Trie).

**Related:** [init-method](init-method.md) · [instance-vs-class-attrs](instance-vs-class-attrs.md)
