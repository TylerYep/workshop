from __future__ import annotations

from dataclasses import dataclass, field

from cs.util import formatter


@dataclass
class Trie:
    """
    Does not use a TrieNode struct because the root node can contain
    several children nodes, thus making the internal logic more complex.
    Instead, sets char to the empty string for the head of the Trie.
    """

    char: str = ""
    is_leaf: bool = False
    size: int = 0
    children: dict[str, Trie] = field(default_factory=dict)

    def __str__(self) -> str:
        return str(formatter.pformat(self))

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
        trie = self
        for ch in prefix:
            if ch not in trie.children:
                return False
            trie = trie.children[ch]
        return trie.is_leaf

    def insert(self, text: str) -> None:
        """
        Inserts a word into the Trie
        :param word: word to be inserted
        :return: None
        """
        trie = self
        for ch in text:
            trie.size += 1
            if ch not in trie.children:
                trie.children[ch] = Trie(ch)
            trie = trie.children[ch]
        trie.is_leaf = True

    def remove(self, word: str) -> None:
        """
        Deletes a word in a Trie
        :param word: word to delete
        :return: None
        """

        def _remove(curr: Trie, word: str) -> bool:
            # If word is empty, attempt to set the word to not a leaf.
            # If the word has no other children,
            # return False so that we can delete above keys.
            curr.size -= 1
            if not word:
                if not curr.is_leaf:
                    return False
                curr.is_leaf = False
                return not curr.children

            ch = word[0]
            if ch not in curr.children:
                return False

            should_delete_curr = _remove(curr.children[ch], word[1:])
            if should_delete_curr:
                del curr.children[ch]
                return not curr.children
            return should_delete_curr

        if word not in self:
            raise KeyError(f"Trie does not contain key: {word}")

        _ = _remove(self, word)
