# for…else (and while…else)

```python
for p in range(2, n):
    if n % p == 0:
        print("composite")
        break
else:                     # runs only if the loop finished WITHOUT break
    print("prime")
```

The `else` on a loop fires when the loop ran to completion — i.e. **no `break` happened**. Read it as "no-break," not "otherwise." It replaces the manual flag pattern (`found = False … if not found:`) in search loops: break when you find the thing, `else` handles the not-found case. Genuinely obscure — plenty of working engineers have never used it — so in interviews the flag variable may communicate better; but recognize it when you see it in editorial code.

**Related:** [for-loop](for-loop.md) · [break-continue](break-continue.md) · [while-loop](while-loop.md)
