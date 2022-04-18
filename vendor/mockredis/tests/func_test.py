from typing import Dict

from vendor.mockredis.tests.conftest import ServerAndAsserterTuple

def test_discard(mockredis_fixture: ServerAndAsserterTuple):
    """Tests discarding all stored data"""
    mockredis_fixture.set_assert("my_key", "my_value")
    mockredis_fixture.set_assert("my_key2", "my_value2")

    mockredis_fixture.server.discard()

    # Cache is now empty
    mockredis_fixture.get_assert("my_key", None)
    mockredis_fixture.get_assert("my_key2", None)

def test_set_and_get(mockredis_fixture: ServerAndAsserterTuple):
    """Tests setting and getting data"""
    mockredis_fixture.server.discard()

    mockredis_fixture.set_assert("Key", "Value")

    mockredis_fixture.get_assert("Key2", None)  # Key doesn't exist

def test_set_and_remove(mockredis_fixture: ServerAndAsserterTuple):
    """Tests setting and removing data"""
    mockredis_fixture.server.discard()

    mockredis_fixture.set_assert("value", "key")

    mockredis_fixture.server.delete("value")

    mockredis_fixture.get_assert("value", None)

def test_hset_and_hgetall(mockredis_fixture: ServerAndAsserterTuple):
    """Tests setting and getting table data"""
    mockredis_fixture.server.discard()

    data = [("a", "z"), ("b", "y"), ("d", "w")]

    for k, v in data:
        mockredis_fixture.server.hset("entry", k, v)

    cached_data = mockredis_fixture.server.hgetall("entry")

    assert isinstance(cached_data, Dict)
    
    for k, v in data:
        assert cached_data[k] == v

    mockredis_fixture.server.delete("entry")

    mockredis_fixture.get_assert("entry", None)