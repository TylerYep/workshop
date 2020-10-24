from src.structures import Trie


class TestTrie:
    @staticmethod
    def test_trie() -> None:
        keys = ["the", "a", "there", "anaswe", "any", "by", "their"]
        t = Trie()
        for key in keys:
            t.insert(key)

        # Search for different keys
        assert len(t) == 7
        assert "the" in t
        assert "these" not in t
        assert "their" in t
        assert "thaw" not in t

        t.remove("by")
        t.remove("the")
        assert len(t) == 5
        assert "by" not in t
        assert "the" not in t

    @staticmethod
    def test_trie_removes() -> None:
        words = "banana bananas bandana band apple all beast".split()
        root = Trie()
        for word in words:
            root.insert(word)

        assert all(word in root for word in words)
        assert "bandanas" not in root
        assert "apps" not in root
        root.remove("all")
        assert "all" not in root
        root.remove("banana")
        assert "banana" not in root
        assert "bananas" in root

    @staticmethod
    def test_repr() -> None:
        words = "t to".split()
        trie = Trie()
        for word in words:
            trie.insert(word)

        assert repr(trie) == (
            "Trie(char='', is_leaf=False, size=2, children={'t': "
            "Trie(char='t', is_leaf=True, size=1, children={'o': "
            "Trie(char='o', is_leaf=True, size=0, children={})})})"
        )
        assert str(trie) == (
            "Trie(\n"
            "    size=2,\n"
            "    children={\n"
            "        't': Trie(\n"
            "            char='t',\n"
            "            is_leaf=True,\n"
            "            size=1,\n"
            "            children={'o': Trie(char='o', is_leaf=True)}\n"
            "        )\n"
            "    }\n"
            ")"
        )
