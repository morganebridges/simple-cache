from unittest import TestCase

from datastore.cache_service import CacheService


class TestCacheService(TestCase):

    def test_set(self):
        cache = CacheService()

        cache.set("one", 1)

        assert cache.get("one") == 1

    def test_unset(self):
        cache = CacheService()

        cache.set("one", 1)

        assert cache.get("one") == 1

        cache.unset("one")

        with self.assertRaises(KeyError):
            cache.get("one")

    def test_nested_commit(self):

        cache = CacheService()

        cache.begin()

        cache.set("one", 1)

        assert cache.get("one") == 1
        cache.begin()

        cache.set("one", 2)

        cache.rollback()

        cache.commit()

        assert cache.get("one") == 1

    def test_multi_value(self):
        cache = CacheService()

        cache.set("ten", 10)

        assert cache.get("ten") == 10

        with self.assertRaises(Exception):
            cache.rollback()
        assert cache.get("ten") == 10

        # start the outer transaction
        cache.begin()
        cache.set("one", 1)

        # start the inner transactiopn
        cache.begin()
        cache.set("one", 2)
        cache.set("ten", 11)
        assert cache.get("one") == 2
        cache.rollback()
        cache.commit()

        assert cache.get("one") == 1, "We expect the cache to get the value from the outer transaction"
        assert cache.get("ten") == 10, "We expect the value we set initially outside of the transaction to be set"

    def test_multi_layer_commit(self):
        cache = CacheService()

        cache.begin()
        cache.set("ten", 10)
        cache.begin()
        cache.set("ten", 9)
        cache.begin()
        cache.set("ten", 8)

        cache.commit()

        assert cache.get("ten") == 8, "Expect the last transaction value to be the committed value"

        assert cache._transactions == 0, "Expect to have committed all open transactions"
        assert cache._cache_stack == [{"ten": 8}], "introspect the internal state of the cache stack"




