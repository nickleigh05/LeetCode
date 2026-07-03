# `import`

```python
import math
math.sqrt(16)      # 4.0 — access via module.name

import heapq as hq   # alias, common for long/frequently-used module names
hq.heappush(...)
```

`import module` loads the whole module and makes its contents accessible through `module.name`. `as` gives it a shorter local alias. Common interview imports: `heapq`, `collections` (`deque`, `Counter`, `defaultdict`), `math`, `itertools`.

**Related:** [from-import](from-import.md)
