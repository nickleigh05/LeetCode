# f-strings

```python
name = "world"
count = 3
f"hello {name}"            # "hello world"
f"{count + 1} items"       # "4 items" — expressions evaluate inline
f"{3.14159:.2f}"           # "3.14" — format spec after the colon
```

An f-string (`f"..."`) evaluates any `{expression}` inside it and substitutes the result. Preferred over `.format()` or `%` for readability and speed.

**Related:** [string-formatting](string-formatting.md) · [string-basics](string-basics.md)
