from typing import List, Optional


class Trie:
    def __init__(self) -> None:
        self.children: List[Optional[Trie]] = [None] * 26
        self.end_of_word = False

    @staticmethod
    def char_to_index(ch: str) -> int:
        """
        Converts key current character into index. Uses only lower case 'a' through 'z'.
        """
        return ord(ch) - ord("a")

    def insert(self, key: str) -> None:
        """
        If not present, inserts key into trie.
        If the key is prefix of trie node, just marks leaf node.
        """
        if not key:
            self.end_of_word = True
            return

        index = self.char_to_index(key[0])
        if self.children[index] is None:
            self.children[index] = Trie()

        child = self.children[index]
        assert isinstance(child, Trie)
        child.insert(key[1:])

    def search(self, key: str) -> bool:
        """ Search key in the trie. Returns true if key is present in trie. """
        if not key:
            return True

        index = self.char_to_index(key[0])
        if self.children[index] is None:
            return False

        child = self.children[index]
        assert isinstance(child, Trie)
        return child.search(key[1:])
