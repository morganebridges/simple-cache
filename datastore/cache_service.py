from copy import deepcopy


class CacheService:

    def __init__(self):
        self._cache_stack: list[dict] = [{}]
        self._transactions = 0

    def set(self, key: str, val: int):
        """
        Put a key into the cache
        ::param: key: A string value that identifies the cache item
        ::param: value: An integer value to be stored in the cache
        """
        self._cache_stack[0][key] = val

    def unset(self, key: str):
        """
        Delete a key from the cache
        :return:
        ::raises: KeyError if the key is not in the cache
        """
        if self._cache_stack:
            del(self._cache_stack[0][key])
        else:
            raise KeyError("Unset key did not exist in the cache")

    def get(self, key: str) -> int:
        """
        get the value for a key in the cache, traversing all open transactions, since
         we are not implementing transaction isolation
        ::raises: KeyError when the value does not exist in the cache
        """
        for version in self._cache_stack:
            if value := version.get(key):
                return value

        raise KeyError("Key did not exist in the cache")

    def begin(self):
        """
        begin a transaction
        """
        self._transactions += 1
        if self._cache_stack:
            self._cache_stack.insert(0, deepcopy(self._cache_stack[0]))
        else:
            self._cache_stack[0] = {}

    def commit(self):
        """
        commit the current transaction
        ::raises Exception if no transaction is active
        """
        if self._transactions:
            # If we have multiple versions, merge the top one down to "commit" the changes
            while self._transactions > 0:
                self._cache_stack[1].update(self._cache_stack.pop(0))
                self._transactions -= 1
        else:
            raise Exception("No transaction in progress")

    def rollback(self):
        """
        rollback the current transaction
        ::raises: Exception if no transaction is active
        """
        if self._transactions:
            if len(self._cache_stack) > 0:
                self._cache_stack.pop(0)
            self._transactions -= 1
        else:
            raise Exception("No transaction in progress")