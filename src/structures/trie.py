from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Union

from src.util import formatter


@dataclass
class TrieNode:
    char: str
    is_leaf: bool = False
    children: Dict[str, TrieNode] = field(default_factory=dict)

    def __repr__(self) -> str:
        return str(formatter.pformat(self))


class Trie:
    """ char is None for the head of the Trie. """

    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.is_leaf = False
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return bool(self.children)

    def __contains__(self, prefix: str) -> bool:
        """
        Tries to find word in a Trie
        :param word: word to look for
        :return: Returns True if word is found, False otherwise
        """
        trie: Union[Trie, TrieNode] = self
        for ch in prefix:
            if ch not in trie.children:
                return False
            trie = trie.children[ch]
        return trie.is_leaf

    def __repr__(self) -> str:
        return str(self.children)

    def insert(self, text: str) -> None:
        """
        Inserts a word into the Trie
        :param word: word to be inserted
        :return: None
        """
        self.size += 1
        trie: Union[Trie, TrieNode] = self
        for ch in text:
            if ch not in trie.children:
                trie.children[ch] = TrieNode(ch)
            trie = trie.children[ch]
        trie.is_leaf = True

    def delete(self, word: str) -> None:
        """
        Deletes a word in a Trie
        :param word: word to delete
        :return: None
        """

        def _delete(curr: Union[Trie, TrieNode], word: str) -> bool:
            # If word is empty, attempt to set the word to not a leaf.
            # If the word has no other children, return False so that we can delete above keys.
            if not word:
                if not curr.is_leaf:
                    return False
                curr.is_leaf = False
                return not curr.children

            ch = word[0]
            if ch not in curr.children:
                return False

            should_delete_curr = _delete(curr.children[ch], word[1:])
            if should_delete_curr:
                del curr.children[ch]
                return not curr.children
            return should_delete_curr

        if word not in self:
            raise KeyError(f"Trie does not contain key: {word}")

        self.size -= 1
        _ = _delete(self, word)
