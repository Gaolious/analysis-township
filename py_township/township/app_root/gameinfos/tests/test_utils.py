import pytest

from app_root.gameinfos.utils import base62_decode, base62_encode, get_ghash, get_whudup


@pytest.mark.parametrize("val, ret", [
    ('1kuxpA', 1609420624),
    ('SZ3', 0)
])
def test_base62_decode(val, ret):
    assert base62_decode(val) == ret


@pytest.mark.parametrize("val, ret", [
    (1609420624, '1kuxpA')
])
def test_base62_encode(val, ret):
    assert base62_encode(val) == ret

@pytest.mark.parametrize("val, ret", [
    (51, -2052240489),
    (35, -146537046),
    (1035, -2801260130),
    (10350, -569316983),
    (199999999, -420063686),
])
def test_ghash(val, ret):
    assert get_ghash(val) == ret


@pytest.mark.parametrize("val, ret", [
    (0, 514698188),
    (1, 514698189),
    (101, 514698153),
])
def test_whudup(val, ret):
    assert get_whudup(val) == ret