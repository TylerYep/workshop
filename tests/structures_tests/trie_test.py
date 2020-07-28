from src.structures.trie import Trie


def trie_test() -> None:
    keys = ["the", "a", "there", "anaswe", "any", "by", "their"]
    t = Trie()
    for key in keys:
        t.insert(key)

    # Search for different keys
    assert t.search("the") is True
    assert t.search("these") is False
    assert t.search("their") is True
    assert t.search("thaw") is False
