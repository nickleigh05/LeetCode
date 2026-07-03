# `match` Statement (Structural Pattern Matching)

```python
match command:
    case "start":
        run()
    case "stop":
        halt()
    case _:
        print("unknown")     # `_` is the wildcard/default case
```

Python's `match`/`case` (3.10+) compares a value against a series of patterns, running the first match — like a more powerful `elif` chain that can also destructure lists/dicts/objects in the `case` pattern itself. Rare in interview code (an `if/elif` chain does the same job and is universally supported), but worth recognizing when reading modern code.

**Related:** [elif-else](elif-else.md)
