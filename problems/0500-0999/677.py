"""

677. Map Sum Pairs

Medium

Design a map that allows you to do the following:

    Maps a string key to a given value.
    Returns the sum of the values that have a key with a prefix equal to a given string.

Implement the MapSum class:

    MapSum() Initializes the MapSum object.
    void insert(String key, int val) Inserts the key-val pair into the map. If the key already
        existed, the original key-value pair will be overridden to the new one.
    int sum(string prefix) Returns the sum of all the pairs' value whose key starts with
        the prefix.

Example 1:

    Input
    ["MapSum", "insert", "sum", "insert", "sum"]
    [[], ["apple", 3], ["ap"], ["app", 2], ["ap"]]
    Output
    [null, null, 3, null, 5]

    Explanation
    MapSum mapSum = new MapSum();
    mapSum.insert("apple", 3);
    mapSum.sum("ap");           // return 3 (apple = 3)
    mapSum.insert("app", 2);
    mapSum.sum("ap");           // return 5 (apple + app = 3 + 2 = 5)

Constraints:

    1 <= key.length, prefix.length <= 50
    key and prefix consist of only lowercase English letters.
    1 <= val <= 1000
    At most 50 calls will be made to insert and sum.

"""

class MapSum:

    def __init__(self):
        self.key_values = {}
        self.prefix_sums = {}

    def insert(self, key: str, val: int) -> None:
        old_val = 0
        if key in self.key_values:
            old_val = self.key_values[key]
        delta = val - old_val
        self.key_values[key] = val

        prefix = ""
        for ch in key:
            prefix += ch
            if prefix in self.prefix_sums:
                self.prefix_sums[prefix] += delta
            else:
                self.prefix_sums[prefix] = delta


    def sum(self, prefix: str) -> int:
        if prefix in self.prefix_sums:
            return self.prefix_sums[prefix]
        return 0


# Your MapSum object will be instantiated and called as such:
# obj = MapSum()
# obj.insert(key,val)
# param_2 = obj.sum(prefix)
























