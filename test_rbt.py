import unittest
import random
import time
from rbt import RedBlackTree


class TestRedBlackTree(unittest.TestCase):

    def setUp(self):
        self.rbt = RedBlackTree()

    def test_insert_and_search(self):
        self.rbt.insert("name", "Alice")
        result = self.rbt.search("name")
        self.assertTrue(result["found"])
        self.assertEqual(result["value"], "Alice")

    def test_search_missing_key(self):
        result = self.rbt.search("ghost")
        self.assertFalse(result["found"])

    def test_update_existing_key(self):
        self.rbt.insert("x", 1)
        self.rbt.insert("x", 99)
        result = self.rbt.search("x")
        self.assertEqual(result["value"], 99)

    def test_delete_existing(self):
        self.rbt.insert("key1", "val1")
        result = self.rbt.delete("key1")
        self.assertEqual(result["action"], "delete")
        self.assertFalse(self.rbt.search("key1")["found"])

    def test_delete_missing(self):
        result = self.rbt.delete("nonexistent")
        self.assertEqual(result["action"], "not_found")

    def test_size_tracking(self):
        for i in range(10):
            self.rbt.insert(f"k{i}", i)
        self.assertEqual(self.rbt.size(), 10)
        self.rbt.delete("k0")
        self.assertEqual(self.rbt.size(), 9)

    def test_root_is_black(self):
        self.rbt.insert("a", 1)
        from rbt import BLACK
        self.assertEqual(self.rbt.root.color, BLACK)

    def test_black_height_invariant_small(self):
        keys = ["mango", "apple", "zebra", "banana", "kiwi"]
        for k in keys:
            self.rbt.insert(k, k)
        result = self.rbt.full_verify()
        self.assertTrue(result["valid"])

    def test_red_property_no_consecutive_reds(self):
        for i in range(100):
            self.rbt.insert(str(random.randint(1, 1000)), i)
        self.assertTrue(self.rbt.verify_red_property())

    def test_black_height_after_deletions(self):
        keys = list(range(50))
        random.shuffle(keys)
        for k in keys:
            self.rbt.insert(str(k), k)
        for k in keys[:25]:
            self.rbt.delete(str(k))
        result = self.rbt.full_verify()
        self.assertTrue(result["valid"])

    def test_10000_random_insertions_black_height(self):
        print("\n[TEST] 10,000 rastgele ekleme...")
        start = time.time()
        keys = random.sample(range(1, 100000), 10000)
        for k in keys:
            self.rbt.insert(str(k), k * 2)
        elapsed = time.time() - start
        result = self.rbt.full_verify()
        print(f"  Süre: {elapsed:.3f}s")
        print(f"  Boyut: {self.rbt.size()}")
        print(f"  Black-Height: {result['black_height']}")
        print(f"  Geçerli: {result['valid']}")
        self.assertEqual(self.rbt.size(), 10000)
        self.assertTrue(result["black_height_valid"])
        self.assertTrue(result["red_property_valid"])
        self.assertTrue(result["root_is_black"])
        self.assertTrue(result["valid"])

    def test_inorder_sorted(self):
        keys = [random.randint(1, 9999) for _ in range(200)]
        for k in keys:
            self.rbt.insert(str(k).zfill(5), k)
        result = self.rbt.all_keys()
        key_list = [r["key"] for r in result]
        self.assertEqual(key_list, sorted(key_list))

    def test_search_ologn(self):
        for i in range(10000):
            self.rbt.insert(str(i), i)
        start = time.time()
        for _ in range(1000):
            self.rbt.search(str(random.randint(0, 9999)))
        elapsed = time.time() - start
        self.assertLess(elapsed, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)