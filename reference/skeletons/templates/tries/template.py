"""
Trie — Prefix Tree Skeleton

A trie stores strings character by character down a tree of nodes, so every
shared prefix is stored exactly once. Looking up a word or a prefix costs O(k)
in the word length k — independent of how many words the trie holds. That is the
whole pitch: prefix queries that never scan the dictionary.

Invariant: the path from the root to any node spells the prefix that node
represents; `is_end` marks the nodes where a complete inserted word terminates.
"""

from typing import Dict, Optional


class TrieNode:
    """One node per character position; children keyed by the next character."""

    def __init__(self) -> None:
        # Maps a single character -> the child node reached by that character.
        self.children: Dict[str, "TrieNode"] = {}
        # True iff some inserted word ends exactly at this node.
        self.is_end: bool = False


class Trie:
    """Insert words and answer exact-word / prefix membership queries."""

    def __init__(self) -> None:
        # The root represents the empty prefix; it never stores a character.
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Add a word, creating nodes for any characters not yet present.

        Time:  O(k), k = len(word).
        Space: O(k) new nodes in the worst case (an entirely new suffix).
        """

        node = self.root
        for character in word:
            # Walk down, creating the branch lazily if this character is new.
            if character not in node.children:
                node.children[character] = TrieNode()
            node = node.children[character]

        # Mark the final node so we can distinguish a stored word from a prefix.
        node.is_end = True

    def _walk(self, prefix: str) -> Optional[TrieNode]:
        """Follow `prefix` from the root; return the node it ends at, or None.

        Shared by search and starts_with — the only difference between them is
        whether we then check `is_end`.
        """

        node = self.root
        for character in prefix:
            if character not in node.children:
                return None  # the path falls off the trie -> prefix absent
            node = node.children[character]
        return node

    def search(self, word: str) -> bool:
        """True iff the exact word was inserted (not merely present as a prefix)."""

        node = self._walk(word)
        # TODO: for wildcard ('.') search, replace _walk with a recursive DFS
        # that branches into every child whenever it meets a '.'.
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """True iff any inserted word begins with `prefix`."""

        return self._walk(prefix) is not None
