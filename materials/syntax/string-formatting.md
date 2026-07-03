# String Formatting

```python
"{} is {}".format("x", 5)     # "x is 5"    — .format()
"%s is %d" % ("x", 5)          # "x is 5"    — % operator, legacy style
f"{'x'} is {5}"                 # "x is 5"    — f-string, modern default
f"{3.14159:.2f}"                # "3.14"      — format spec
f"{42:04d}"                     # "0042"      — zero-padded
```

Three ways to build formatted strings; f-strings ([f-strings](f-strings.md)) are the modern default for readability and speed. `.format()` and `%` still appear in older code and are worth recognizing.

**Related:** [f-strings](f-strings.md) · [string-basics](string-basics.md)
