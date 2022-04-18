from typing import NamedTuple

import pytest

from ..mockserver import MockServer


class SetAndGetAsserter:

    def __init__(self, setter, getter):
        self.setter = setter
        self.getter = getter

    def set(self, key, value):
        self.setter(key, value)
        self.get(key, value)

    def get(self, key, value):
        val = self.getter(key)
        assert val == value
        return val

        
class ServerAndAsserterTuple(NamedTuple):
    server: MockServer
    asserter: SetAndGetAsserter

    def set_assert(self, key, value):
        self.asserter.set(key, value)

    def get_assert(self, key, value):
        return self.asserter.get(key, value)


@pytest.fixture()
def mockredis_fixture():
    server = MockServer()
    return ServerAndAsserterTuple(server=server, asserter=SetAndGetAsserter(server.set, server.get))