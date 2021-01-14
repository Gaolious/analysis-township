import pytest

from modules.ts_utils import *

VALUE_RANGE = [
    -1, 0, 1,
    -128, 127, 255,
    -32768, 32767, 65535,
    -2147483648, 2147483647, 4294967295,
    -9223372036854775808, 9223372036854775807, 18446744073709551615,
]
DELTA_RANGE = [
    -1, 0, 1
]


@pytest.mark.parametrize("value", VALUE_RANGE)
@pytest.mark.parametrize("delta", DELTA_RANGE)
def test_bitmask(value, delta):

    ret = u8(value + delta)
    assert 0 <= ret <= 255

    ret = u16(value + delta)
    assert 0 <= ret <= 65535

    ret = u32(value + delta)
    assert 0 <= ret <= 4294967295

    ret = u64(value + delta)
    assert 0 <= ret <= 18446744073709551615

    ret = s8(value + delta)
    assert -128 <= ret <= 127

    ret = s16(value + delta)
    assert -32768 <= ret <= 32767

    ret = s32(value + delta)
    assert -2147483648 <= ret <= 2147483647

    ret = s64(value + delta)
    assert -9223372036854775808 <= ret <= 9223372036854775807


@pytest.mark.parametrize("value", VALUE_RANGE)
@pytest.mark.parametrize("delta", DELTA_RANGE)
def test_byte(value, delta):
    x = value+delta
    ret = RB0(x)
    assert (x & 0xFF) == ret
    assert u8(ret) == ret

    x = value+delta
    ret = RB1(x)
    assert (x & 0xFF00) >> 8 == ret
    assert u8(ret) == ret

    x = value+delta
    ret = RB2(x)
    assert (x & 0xFF0000) >> 16 == ret
    assert u8(ret) == ret

    x = value+delta
    ret = RB3(x)
    assert (x & 0xFF000000) >> 24 == ret
    assert u8(ret) == ret



@pytest.mark.parametrize("value, ret",[
    ("58 E2 6F AD F0 DB 6F AD B8 2A 28 A4 B4 2D F5 AC", b"\x58\xE2\x6F\xAD\xF0\xDB\x6F\xAD\xB8\x2A\x28\xA4\xB4\x2D\xF5\xAC")
])
def test_hex_dump_to_bytes(value, ret):
    assert hex_dump_to_bytes(value) == ret


@pytest.mark.parametrize("value, ret", [
    (0x11223344,0x44332211)
])
def test_ReverseU32(value, ret):
    assert ReverseU32(value) == ret


def test_bytearray_parameter_check():
    data = bytearray.fromhex("0011223344")

    def check(param):
        param[0] = 0xFF

    check(data)
    assert data[0] == 0xFF

def test_list_copy_and_reference_check():
    a = [i for i in range(10)]
    b = []
    for i in range(3):
        b.append(a[i:i+5])

    a[0] = 10

    assert b[0][0] == 0


@pytest.mark.parametrize("a,b,c, ret", [
    (0x01234567, 0x89ABCDEF, 4, 0x12345678),
    (0x01234567, 0x89ABCDEF, 8, 0x23456789),
    (0x01234567, 0x89ABCDEF, 12, 0x3456789A),
])
def test_shld(a, b, c, ret):
    assert ret == shld(a, b, c)


@pytest.mark.parametrize("a,b,c, ret", [
    (0x01234567, 0x89ABCDEF, 4, 0xF0123456),
    (0x01234567, 0x89ABCDEF, 8, 0xEF012345),
    (0x01234567, 0x89ABCDEF, 12, 0xDEF01234),
])
def test_shld(a, b, c, ret):
    assert ret == shrd(a, b, c)

@pytest.mark.parametrize("data, s, ret", [
    (0b11110000, 1, 0b11100001),
    (0b11110000, 2, 0b11000011),
    (0b11110000, 3, 0b10000111),
    (0b11110000, 4, 0b00001111),
    (0b11110000, 5, 0b00011110),
    (0b11110000, 6, 0b00111100),
    (0b11110000, 7, 0b01111000),
    (0b11110000, 8, 0b11110000),
    (0b11110000, 9, 0b11100001),
])
def test_ROL8(data, s, ret):
    assert ROL8(data=u8(data), shift=s) == u8(ret)


@pytest.mark.parametrize("data, s, ret", [
    (0b11110000, 1, 0b01111000),
    (0b11110000, 2, 0b00111100),
    (0b11110000, 3, 0b00011110),
    (0b11110000, 4, 0b00001111),
    (0b11110000, 5, 0b10000111),
    (0b11110000, 6, 0b11000011),
    (0b11110000, 7, 0b11100001),
    (0b11110000, 8, 0b11110000),
    (0b11110000, 9, 0b01111000),
])
def test_ROR8(data, s, ret):
    assert ROR8(data=u8(data), shift=s) == u8(ret)

# def ROL8(data, shift):
#     size = 8
#     shift %= size
#     return u8((data << shift)) | u8(data >> (size - shift))
#
#
# def ROR8(data, shift):
#     size = 8
#     shift %= size
#     return u8((data >> shift)) | u8(data << (size - shift))
