from typing import Dict, NamedTuple, Any

class MockServer:

    class DBEntry(NamedTuple):
        value: str|Dict[str, str|Any]
        expiry: int

        def __str__(self):
            return f"(value={self.value}, expiry={self.expiry})"

    ## Actual class functions and variables: ##

    __cache: Dict[int, Dict[str, DBEntry]] = {}


    def __init__(self, host="localhost", port=6379, db=0, default_expire=60*60, **kwargs):
        self.host = host
        self.port = port
        self.db = db
        self.default_expire = default_expire
        """Todo: Add expiring to keys in the cache. This probably isn't urgent, as this is only
        meant to be used for testing, and tests would most likely outlast the expiry value.
        """

        for k,w in kwargs.items():
            setattr(self, k, w)

    def ping(self, *a, **kw):
        return True

    @property
    def __db(self) -> Dict[str, str|Any]:
        if MockServer.__cache.get(self.db) == None:
            MockServer.__cache[self.db] = {}

        return MockServer.__cache[self.db] 

    def set(self, key: str, value: Any, expiry:int = None) -> None:
        self.__db[key] = MockServer.DBEntry(str(value), expiry or self.default_expire)

    def get(self, key) -> str|None:
        entry = self.__db.get(key)
        return entry.value if entry is not None else None

    def delete(self, *keys) -> None:
        for key in keys:
            self.__db.pop(key, None)

    def hset(self, name: str, key:str = None, value:str = None, mapping=None) -> None:
        if mapping is not None:
            raise NotImplementedError("MockServer.hset has no custom mapping implementation!")

        if key is None and not mapping:
            raise ValueError("'hset' with no key value pairs")

        if self.__db.get(name) == None:
            self.__db[name] = MockServer.DBEntry({}, 0xFFFFFFFF) # Max 32 unsigned integer time
        elif isinstance(self.__db.get(name), str):
            raise TypeError("Entry already exists as a non-dict type. Perhaps this is intended behavior?")

        self.__db[name].value[key] = str(value)

    def hgetall(self, name: str) -> Dict[str, str|Any] | None:
        return self.__db[name].value if self.__db.get(name) else None

    def discard(self) -> None:
        self.__db.clear()



        

        

        
