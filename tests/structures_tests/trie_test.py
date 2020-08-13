from src.structures import Trie


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

    t.delete("by")
    t.delete("the")
    assert len(t) == 5
    assert "by" not in t
    assert "the" not in t


def test_trie_deletes() -> None:
    words = "banana bananas bandana band apple all beast".split()
    root = Trie()
    for word in words:
        root.insert(word)

    assert all(word in root for word in words)
    assert "bandanas" not in root
    assert "apps" not in root
    root.delete("all")
    assert "all" not in root
    root.delete("banana")
    assert "banana" not in root
    assert "bananas" in root
