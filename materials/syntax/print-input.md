# print() and input()

```python
print("hello")                      # hello
print("a", "b", 3)                  # a b 3        (spaces between, newline after)
print("a", "b", sep="-", end="!\n") # a-b!         (customize both)
print(*[1, 2, 3])                   # 1 2 3        (unpack a list into args)

name = input("Your name: ")         # shows prompt, returns what was typed — always a str
age = int(input())                  # convert yourself; input() never returns numbers
```

`print` writes to the screen, `input` reads a line of typed text (always as a string — [convert](type-conversion.md) explicitly). On LeetCode you use neither for answers — the judge calls your function and takes the **return value** — so `print` is purely a [debugging](../guides/debugging-python.md) tool there, and `input` only matters on other judges ([competitive I/O](../guides/competitive-programming-io.md)).

**Related:** [f-strings](f-strings.md) · [type-conversion](type-conversion.md) · [variables-assignment](variables-assignment.md)
