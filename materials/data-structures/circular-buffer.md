# Circular Buffer (Ring Buffer)

```python
class CircularQueue:                    # LC 622, Design Circular Queue
    def __init__(self, k):
        self.buf = [0] * k
        self.head = 0                   # index of front
        self.size = 0
        self.k = k

    def enqueue(self, v):
        if self.size == self.k: return False
        self.buf[(self.head + self.size) % self.k] = v   # ★ wrap with modulo
        self.size += 1
        return True

    def dequeue(self):
        if self.size == 0: return False
        self.head = (self.head + 1) % self.k
        self.size -= 1
        return True
```

A fixed-size array pretending to be an endless [queue](queue.md): indices wrap around via `% k`, so the front chases the back around a ring and no element ever shifts. This is how real systems implement bounded queues (audio buffers, keyboard input, network packets, log-of-last-N) — O(1) operations, zero allocation after startup, and old data naturally overwritten when you choose overwrite-on-full semantics. In Python practice you'd normally grab [`deque(maxlen=k)`](../syntax/deque-basics.md), which is exactly this; the hand-rolled version is what LC 622 and "design a bounded queue, no library" interviews want — the whole trick being the two `% k` lines.

**Complexity:** enqueue/dequeue/front/rear O(1) · space O(k) fixed.

**Related:** [queue](queue.md) · [deque](deque.md) · [array](array.md) · [integer-division-modulo (syntax)](../syntax/integer-division-modulo.md)
