# `finally`

```python
try:
    file = open("data.txt")
    process(file)
except FileNotFoundError:
    print("missing file")
finally:
    file.close()          # always runs — success, exception, or return
```

Code in `finally` runs no matter what happens in `try`/`except` — whether it succeeded, raised an exception, or hit a `return`. Used for cleanup that must always happen (closing files/connections), regardless of how the block exits.

**Related:** [try-except](try-except.md)
