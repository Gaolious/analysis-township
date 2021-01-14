import time
from ctypes import c_int8, c_int16, c_int32, c_int64, c_uint16, c_uint8, c_uint32, c_uint64
from datetime import datetime
from struct import unpack
from typing import Union, List

import pytz
from django.utils import timezone

orda = ord('a')
ordz = ord('z')
ordA = ord('A')
ordZ = ord('Z')
ord0 = ord('0')
ord9 = ord('9')

#######################################################################
# bit mask
#######################################################################

def s8(x: int) -> int: return c_int8(x).value


def s16(x: int) -> int: return c_int16(x).value


def s32(x: int) -> int: return c_int32(x).value


def s64(x: int) -> int: return c_int64(x).value


def u8(x: int) -> int: return c_uint8(x).value


def u16(x: int) -> int: return c_uint16(x).value


def u32(x: int) -> int: return c_uint32(x).value


def u64(x: int) -> int: return c_uint64(x).value


def u128(x: int) -> int: return x & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

#######################################################################
# SHR
#######################################################################
def RBn(x: int, n: int) -> int:
    x = x >> (n * 8)
    return u8(x)


def RB0(x: int) -> int: return RBn(x, 0)


def RB1(x: int) -> int: return RBn(x, 1)


def RB2(x: int) -> int: return RBn(x, 2)


def RB3(x: int) -> int: return RBn(x, 3)


def ROL8(data, shift):
    size = 8
    shift %= size
    return u8((data << shift)) | u8(data >> (size - shift))


def ROR8(data, shift):
    size = 8
    shift %= size
    return u8((data >> shift)) | u8(data << (size - shift))

#######################################################################
# SHL
#######################################################################
def LBn(x: int, n: int) -> int:
    x = u8(x) << (n * 8)
    return u32(x)


def LB0(x: int) -> int: return LBn(x, 0)


def LB1(x: int) -> int: return LBn(x, 1)


def LB2(x: int) -> int: return LBn(x, 2)


def LB3(x: int) -> int: return LBn(x, 3)


#######################################################################
# merge & shift bit
#######################################################################
def __PAIR__(a: int, b: int) -> int:
    ret = (u32(a) << 32) | u32(b)
    return ret


def __PAIR_R__(a: int, b: int, c) -> int:
    ret = u64(__PAIR__(a, b)) >> c
    return ret


def __PAIR_R1__(a: int, b: int) -> int: return __PAIR_R__(a, b, 1)


def __PAIR_R2__(a: int, b: int) -> int: return __PAIR_R__(a, b, 2)


def __PAIR_R3__(a: int, b: int) -> int: return __PAIR_R__(a, b, 3)


def __PAIR_R4__(a: int, b: int) -> int: return __PAIR_R__(a, b, 4)


def shld(a: int, b: int, c: int):
    s = 32
    c %= s

    _a = a << c
    _b = b << c
    _a |= b >> (s - c)
    _b |= a >> (s - c)
    return u32(_a)


def shrd(a: int, b: int, c: int):
    s = 32
    c %= 32

    _a = a >> c
    _b = b >> c
    _a |= b << (s - c)
    _b |= a << (s - c)
    return u32(_a)


#######################################################################
# SHR
#######################################################################
def sethibyte(a, val): return (u32(a) & 0x00FFFFFF) | LB3(u8(val))


def setlobyte(a, val): return (u32(a) & 0xFFFFFF00) | LB0(u8(val))


def setbyte0(a, val): return (u32(a) & 0xFFFFFF00) | LB0(u8(val))


def setbyte1(a, val): return (u32(a) & 0xFFFF00FF) | LB1(u8(val))


def setbyte2(a, val): return (u32(a) & 0xFF00FFFF) | LB2(u8(val))


def setbyte3(a, val): return (u32(a) & 0x00FFFFFF) | LB3(u8(val))


# #######################################################################
# # Convert Bytes to (1,2,4,8,16) bytes single Integer
# #######################################################################
# def uLEPtr(x: Union[bytes, bytearray], n: int, offset: int) -> int:
#     return int.from_bytes(
#         bytes=x[offset:offset+n],
#         byteorder='little'
#     )
#
#
# # x[offset : offset + 1] to uint8
# def toU8(x: Union[bytes, bytearray], offset: int) -> int: return uLEPtr(x, 1, 0)
#
#
# # x[offset : offset + 2] to uint16
# def toU16(x: Union[bytes, bytearray], offset: int) -> int: return uLEPtr(x, 2, 0)
#
#
# # x[offset : offset + 4] to uint32
# def toU32(x: Union[bytes, bytearray], offset: int) -> int: return uLEPtr(x, 4, 0)
#
#
# # x[offset : offset + 8] to uint64
# def toU64(x: Union[bytes, bytearray], offset: int) -> int: return uLEPtr(x, 8, 0)
#
#
# # x[offset : offset + 16] to uint128
# def toU128(x: Union[bytes, bytearray], offset: int) -> int: return uLEPtr(x, 16, 0)


#######################################################################
# Convert Bytes to (1,2,4,8) bytes Integer List
#######################################################################
def toU8List(x: Union[bytes, bytearray]) -> List[int]:
    return list(unpack('B' * (len(x)), x))


def toU16List(x: Union[bytes, bytearray]) -> List[int]:
    assert len(x) % 2 == 0
    return list(unpack('H' * (len(x)//2), x))


def toU32List(x: Union[bytes, bytearray]) -> List[int]:
    assert len(x) % 4 == 0
    return list(unpack('I' * (len(x)//4), x))


def toU64List(x: Union[bytes, bytearray]) -> List[int]:
    assert len(x) % 8 == 0
    return list(unpack('Q' * (len(x)//8), x))


#######################################################################
# byte swap
#######################################################################
def ReverseU32(n: int) -> int:
    """
        input
            n = 0x11223344
        output
            0x44332211
    """
    ret = 0
    return int.from_bytes(
        bytes=n.to_bytes(length=4, byteorder='little'),
        byteorder='big'
    )


#######################################################################
# dump
#######################################################################
def hex_dump_to_bytes(str_in: str) -> bytearray:
    """
        In
            "58 E2 6F AD F0 DB 6F AD B8 2A 28 A4 B4 2D F5 AC"
        Out
            b"\x58\xE2\x6F\xAD\xF0\xDB\x6F\xAD\xB8\x2A\x28\xA4\xB4\x2D\xF5\xAC")
    """
    s = str_in.replace(' ', '').replace('\n', '')
    return bytearray().fromhex(s)


def hexdump(string: bytes):
    len_str = len(string)

    print('\n{0:6s} | {1:s} | {2:s}'.format(' ', ' '.join(['{0:2X}'.format(i) for i in range(16)]), ''))
    print("-"*6 + '-+-' + '---'*16 + '+-' + '-'*16 + '-')
    for idx in range(0, len_str, 16):
        print('{0:06x} | {1} | {2}'.format(
            idx,
            ' '.join(['{0:02x}'.format(string[i]) if len_str > i else '  ' for i in range(idx, idx+16)]),
            ''.join([chr(string[i]) if chr(string[i]).isprintable() else '.' for i in range(idx, min(len_str,idx+16))])
        ))


def timestamp_to_datetime(ts: float):
    datetime.fromtimestamp(ts, pytz.timezone('Asia/Seoul'))


def datetime_to_timestamp(dt: datetime):
    return time.mktime(dt.timetuple())
