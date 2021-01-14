from __future__ import annotations
from typing import Union, Optional, NoReturn, List

from modules.ts_utils import u32, u8, u16, u64


__STR_SIZE__ = 40


class Structure(object):

    def get(self, offset, nbytes) ->int : pass
    def set(self, offset, val, nbytes): pass

    def __len__(self):
        return 0


class bytePtr(object):
    """
        Usage :
            _byte data[0xFF]
    """
    _obj: Optional[Structure] = None
    _size: int = 0
    _offset: int = 0

    def __len__(self):
        return len(self._obj) - self._offset

    def __init__(self, obj, size, offset = 0):
        self._obj = obj
        self._size = size
        self._offset = offset

    def __str__(self):
        return '{0}B +0x{1:x} {2}'.format(self._size, self._offset, self._obj)

    def __getitem__(self, key: int):
        offset = self._offset + key * self._size
        return self._obj.get(offset, self._size)

    def __setitem__(self, key, value):
        offset = self._offset + key * self._size
        self._obj.set(offset, value, self._size)

    @property
    def as_u8(self) -> bytePtr:
        return bytePtr(self._obj, 1, self._offset)

    @property
    def as_u16(self) -> bytePtr:
        return bytePtr(self._obj, 2, self._offset)

    @property
    def as_u32(self) -> bytePtr:
        return bytePtr(self._obj, 4, self._offset)

    @property
    def as_u64(self) -> bytePtr:
        return bytePtr(self._obj, 8, self._offset)

    @property
    def as_u128(self) -> bytePtr:
        return bytePtr(self._obj, 16, self._offset)

    def byte_offset(self, nbytes):
        return bytePtr(self._obj, self._size, self._offset + nbytes)

    def offset(self, nbytes):
        return bytePtr(self._obj, self._size, self._offset + self._size * nbytes)

    def clone(self):
        return bytePtr(self._obj, self._size, self._offset)

    def getBytearray(self, n=0):
        if n <= 0:
            n = self._size
        return self._obj.getBytearray(self._offset, n)

    def data(self) ->bytearray:
        return self._obj.data()

class byteClass(Structure):
    _data: Optional[bytearray] = None
    _count: int = 0

    def __init__(self, data: Union[bytearray, bytes]):
        self._data = bytearray(data) if isinstance(data, bytes) else data
        self._count = len(data) if data else 0

    def __len__(self):
        return self._count

    def __ne__(self, other):
        if not isinstance(other, byteClass):
            return True
        if self._count != other._count:
            return True
        if self._data != other._data:
            return True
        return False

    def __eq__(self, other):
        return not self.__ne__(other)

    def __str__(self):
        if self._count >= __STR_SIZE__:
            return '{0}...'.format(self._data[:__STR_SIZE__-3].hex())
        else:
            return '{0}'.format(self._data.hex())

    @classmethod
    def fromInt128(cls, n):
        t = cls(bytes([0] * 16))
        t.as_u128[0] = n
        return t

    @classmethod
    def fromInt64(cls, n):
        t = cls(bytes([0] * 8))
        t.as_u64[0] = n
        return t

    @classmethod
    def fromInt32(cls, n):
        t = cls(bytes([0] * 4))
        t.as_u32[0] = n
        return t

    @classmethod
    def fromhex(cls, s:str):
        obj = cls(None)
        obj._data = bytearray.fromhex(s)
        obj._count = len(obj._data)
        return obj

    def capacity(self, size):
        self._count = size
        self._data = bytearray([0] * size)

    def get(self, offset, nbytes):
        ret = 0
        for i in range(nbytes-1, -1, -1):
            assert 0 <= offset + i < self._count, "size=0x{0:x} / offset=0x{1:x} / write length=0x{2:x}".format(self._count, offset, nbytes)

            ret = (ret << 8) | self._data[offset + i]
        return ret

    def set(self, offset, val, nbytes):
        for i in range(0, nbytes):
            assert 0 <= offset + i < self._count, "size=0x{0:x} / offset=0x{1:x} / write length=0x{2:x} / value=0x{3:x}".format(self._count, offset, nbytes, val)
            _val = val >> (8 * i)
            self._data[offset + i] = u8(_val)

    def getBytearray(self, offset, n):
        assert 0 <= offset
        assert offset + n < self._count

        return self._data[offset:offset+n]

    def data(self) -> bytearray:
        return self._data

    @property
    def u8(self) -> bytePtr:
        return bytePtr(self, 1)

    @property
    def u16(self) -> bytePtr:
        return bytePtr(self, 2)

    @property
    def u32(self) -> bytePtr:
        return bytePtr(self, 4)

    @property
    def u64(self) -> bytePtr:
        return bytePtr(self, 8)

    @property
    def u128(self) -> bytePtr:
        return bytePtr(self, 16)

    @property
    def as_u8(self) -> bytePtr:
        return bytePtr(self, 1, 0)

    @property
    def as_u16(self) -> bytePtr:
        return bytePtr(self, 2, 0)

    @property
    def as_u32(self) -> bytePtr:
        return bytePtr(self, 4, 0)

    @property
    def as_u64(self) -> bytePtr:
        return bytePtr(self, 8, 0)

    @property
    def as_u128(self) -> bytePtr:
        return bytePtr(self, 16, 0)

    def with_offset_u8(self, offset) -> bytePtr:
        return bytePtr(self, 1, offset)

    def with_offset_u16(self, offset) -> bytePtr:
        return bytePtr(self, 2, offset)

    def with_offset_u32(self, offset) -> bytePtr:
        return bytePtr(self, 4, offset)

    def with_offset_u64(self, offset) -> bytePtr:
        return bytePtr(self, 8, offset)

    def with_offset_u128(self, offset) -> bytePtr:
        return bytePtr(self, 16, offset)


def memcpy(dst:bytePtr, src:bytePtr, n:int):
    assert isinstance(dst, bytePtr)
    assert isinstance(src, bytePtr)

    assert len(dst) >= n
    assert len(src) >= n

    dst = dst.as_u8
    src = src.as_u8

    for i in range(n):
        dst[i] = src[i]