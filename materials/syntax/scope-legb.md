# Scope: the LEGB Rule

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)          # "local" — found at L, search stops
    inner()

# Name lookup order:  Local → Enclosing → Global → Built-in
```

When Python sees a name, it searches four layers in order: the current function (**L**ocal), any surrounding functions (**E**nclosing), the module (**G**lobal), then Python itself (**B**uilt-in — `len`, `max`, `sum`). Two practical consequences: a nested DFS helper can *read* its parent's variables freely (that's the E layer — see [closures](closures.md)), but *assigning* creates a new local unless declared [nonlocal/global](global-nonlocal.md); and naming a variable `list`, `sum`, or `max` shadows the built-in for the rest of the scope — `sum = 0` then `sum(nums)` → `TypeError: 'int' object is not callable`.

**Related:** [global-nonlocal](global-nonlocal.md) · [closures](closures.md) · [function-basics](function-basics.md)
