from typing import List, NoReturn, Union

from django.conf import settings

from modules.ts_aes_data import T1, T4, Tb3, Tb2, Tb1, Rc, T2, T3, T
from modules.ts_bytes import byteClass, bytePtr, memcpy
from modules.ts_utils import ReverseU32, LB0, RB3, LB1, RB2, LB2, RB1, LB3, RB0, toU32List, u32, __PAIR_R1__, sethibyte, \
    shld, RBn, u8, hexdump, u128



def _mm_loadu_si128(mem_addr: bytePtr) -> int:
    return mem_addr.as_u128[0]


def _mm_load_si128(mem_addr: bytePtr) -> int:
    return mem_addr.as_u128[0]


def _mm_store_si128(mem_addr: bytePtr, a: int) -> NoReturn:
    memcpy(mem_addr, byteClass.fromInt128(a).u8, 16)


def _mm_storeu_si128(mem_addr: bytePtr, a: int) -> NoReturn:
    memcpy(mem_addr, byteClass.fromInt128(a).u8, 16)


def _mm_slli_epi64(_val: int, _n: int) -> int:
    a = byteClass.fromInt128(_val)
    a.as_u64[1] <<= _n
    return a.as_u128[0]


def _mm_srli_epi64(_val: int, _n: int) -> int:
    _a = byteClass.fromInt128(_val)
    _a.as_u64[1] >>= _n
    return _a.as_u128[0]


def _mm_xor_si128(_a: int, _b: int) -> int:
    return u128(_a ^ _b)


def _mm_or_si128(_a: int, _b: int) -> int:
    return u128(_a | _b)


def _mm_and_si128(_a: int, _b: int) -> int:
    return u128(_a & _b)


def aes_xmm(_a1: bytePtr):
    """
        ver 7.9.0 : .text:02425EEF aes_encode_xmm
    """

    xmmword_0284FBE0 = 0x00000000FF00000000000000FF000000
    xmmword_0284F970 = 0x0000000000FF00000000000000FF0000
    xmmword_0284FBC0 = 0x000000000000FF00000000000000FF00
    xmmword_0284FBD0 = 0x00000000000000FF00000000000000FF

    a1 = _a1.as_u128

    v3 = _mm_loadu_si128(a1.offset(3))
    _mm_storeu_si128(a1.offset(3), _mm_slli_epi64(v3, 3))

    if a1.offset(22).as_u32[2] or a1.offset(22).as_u32[3]:
        InvMix_1(a1.offset(4), a1.offset(6))

    v6 = _mm_srli_epi64(v3, 5)
    v8 = _mm_srli_epi64(v3, 0x15)
    _mm_storeu_si128(
        a1.offset(4),
        _mm_xor_si128(
            _mm_loadu_si128(a1.offset(4)),
            _mm_or_si128(
                _mm_or_si128(
                    _mm_or_si128(
                        _mm_or_si128(
                            _mm_and_si128(v6, xmmword_0284FBE0),
                            _mm_and_si128(
                                _mm_srli_epi64(v3, 0x25), xmmword_0284FBC0)
                        ),
                        _mm_and_si128(
                            _mm_srli_epi64(v3, 0x35), xmmword_0284FBD0)
                    ),
                    _mm_slli_epi64(
                        _mm_or_si128(
                            _mm_or_si128(
                                _mm_and_si128(v8, xmmword_0284FBD0),
                                _mm_or_si128(
                                    _mm_and_si128(v6, xmmword_0284FBC0),
                                    _mm_slli_epi64(v3, 0x1B)
                                )
                            ),
                            _mm_and_si128(
                                _mm_slli_epi64(v3, 0xB),
                                xmmword_0284F970
                            )
                        ),
                        0x20
                    )
                ),
                _mm_and_si128(v8, xmmword_0284F970)
            )
        )
    )

    InvMix_1(a1.offset(4), a1.offset(6))

    a1.offset(4).as_u128[0] ^= a1.offset(2).as_u128[0]


def InvMix_1(a1: bytePtr, a2: bytePtr):
    """
        ver 7.9.0 : .text:02424E15 sub_2424E15     proc near
    """
    d0, d1, d2, d3 = 0, 0, 0, 0

    u8a1 = a1.as_u8
    u32a1 = a1.as_u32
    u32a2 = a2.as_u32

    for i in range(15, -1, -1):
        idx = (u8a1[i] & 0xF) << 2
        s0 = u32a2[idx + 0] ^ shld(d0, d1, 0x1C)
        s1 = u32a2[idx + 1] ^ T[d3 & 0xF] ^ (d0 >> 4)
        s2 = u32a2[idx + 2] ^ shld(d2, d3, 0x1C)
        s3 = u32a2[idx + 3] ^ shld(d1, d2, 0x1C)

        idx = (u8a1[i] & 0xF0) >> 2
        d0 = u32a2[idx + 1] ^ T[s2 & 0xF] ^ (s1 >> 4)
        d1 = u32a2[idx + 0] ^ shld(s1, s0, 0x1C)
        d2 = u32a2[idx + 3] ^ shld(s0, s3, 0x1C)
        d3 = u32a2[idx + 2] ^ shld(s3, s2, 0x1C)

    u32a1[0] = ReverseU32(d0)
    u32a1[1] = ReverseU32(d1)
    u32a1[2] = ReverseU32(d2)
    u32a1[3] = ReverseU32(d3)

    return d3 >> 16


def InvMix_2(a1: bytePtr, a2: bytePtr, a3: bytePtr, n):
    """
        ver 7.9.0 : .text:024250A3 sub_24250A3
    """
    u8a2 = a2.as_u8
    u8a3 = a3.as_u8

    u32a1 = a1.as_u32
    u32a2 = a2.as_u32

    for _ in range(0, n, 16):
        d0, d1, d2, d3 = 0, 0, 0, 0

        for i in range(15, -1, -1):
            v7 = u8a2[i] ^ u8a3[i]
            idx = (v7 & 0xF) << 2
            s0 = u32a1[idx + 0] ^ shld(d0, d1, 0x1C)
            s1 = u32a1[idx + 1] ^ T[d3 & 0xF] ^ (d0 >> 4)
            s2 = u32a1[idx + 2] ^ shld(d2, d3, 0x1C)
            s3 = u32a1[idx + 3] ^ shld(d1, d2, 0x1C)

            idx = (v7 & 0xF0) >> 2
            d0 = u32a1[idx + 1] ^ T[s2 & 0xF] ^ (s1 >> 4)
            d1 = u32a1[idx + 0] ^ shld(s1, s0, 0x1C)
            d2 = u32a1[idx + 3] ^ shld(s0, s3, 0x1C)
            d3 = u32a1[idx + 2] ^ shld(s3, s2, 0x1C)

        u32a2[0] = ReverseU32(d0)
        u32a2[1] = ReverseU32(d1)
        u32a2[2] = ReverseU32(d2)
        u32a2[3] = ReverseU32(d3)

        u8a3 = u8a3.byte_offset(16)

    return 0


class AES_CTX(object):
    ROUND_MAP = {128: 0x0A, 192: 0x0C, 256: 0x0E}
    _data:byteClass = None

    def __init__(self):
        super(AES_CTX, self).__init__()
        self._data = byteClass(bytearray([0] * 244))

    def __ne__(self, other):
        if not isinstance(other, AES_CTX):
            return True
        if self._data != other._data:
            return True
        return False

    def __eq__(self, other):
        return not self.__ne__(other)

    @classmethod
    def from_bytes(cls, data: bytes):  # for pytest
        assert len(data) == 4 * 60 + 4
        obj = cls()
        obj._data = byteClass(data)
        return obj

    @classmethod
    def from_hex(cls, data: str):  # for pytest
        assert len(data) == 2 * (4 * 60 + 4), "AES_CTX size is 244, hexString(488), but parameter is {}".format(len(data))
        obj = cls().from_bytes(bytes.fromhex(data))
        return obj

    @property
    def rounds(self):
        return self._data.u32[60]

    @rounds.setter
    def rounds(self, val):
        self._data.u32[60] = val

    @property
    def rd_key(self):
        return self._data.u32

    def set_encrypt_key(self, userKey: bytePtr, bits: int):
        """
            ver 7.9.0 : .text:02431A14 sub_2431A14     proc near
        """
        self.rounds = self.ROUND_MAP[bits]
        key32 = userKey.as_u32

        if bits == 0x80:
            for i in range(0, 4):
                self.rd_key[i] = ReverseU32(key32[i])

            for i in range(0, 0x28, 4):
                v6 = self.rd_key[i + 3]
                v4 = LB0(T4[RB3(v6)]) ^ LB1(Tb3[RB0(v6)]) ^ LB2(Tb2[RB1(v6)]) ^ LB3(Tb1[RB2(v6)])
                self.rd_key[i + 4] = self.rd_key[i + 0] ^ v4 ^ Rc[i // 4]
                self.rd_key[i + 5] = self.rd_key[i + 1] ^ self.rd_key[i + 4]
                self.rd_key[i + 6] = self.rd_key[i + 2] ^ self.rd_key[i + 5]
                self.rd_key[i + 7] = self.rd_key[i + 3] ^ self.rd_key[i + 6]

    def single_block_encrypt(self, a1: bytePtr, a2: bytePtr):
        rk_idx = 0
        d0, d1, d2, d3 = 0, 0, 0, 0
        in32 = a1.as_u32
        out32 = a2.as_u32

        def X(a, b, c, d):
            return T1[RB1(a)] ^ T2[RB0(b)] ^ T3[RB3(c)] ^ T4[RB2(d)]

        def O(a, b, c, d):
            return LB3(Tb1[RB3(a)]) | LB2(Tb2[RB2(b)]) | LB1(Tb3[RB1(c)]) | LB0(T4[RB0(d)])

        s0 = self.rd_key[rk_idx + 0] ^ ReverseU32(in32[0])
        s1 = self.rd_key[rk_idx + 1] ^ ReverseU32(in32[1])
        s2 = self.rd_key[rk_idx + 2] ^ ReverseU32(in32[2])
        s3 = self.rd_key[rk_idx + 3] ^ ReverseU32(in32[3])

        for i in range(0, self.rounds // 2):
            rk_idx += 4
            d3 = self.rd_key[rk_idx + 0] ^ X(s2, s3, s0, s1)
            d2 = self.rd_key[rk_idx + 1] ^ X(s3, s0, s1, s2)
            d1 = self.rd_key[rk_idx + 2] ^ X(s0, s1, s2, s3)
            d0 = self.rd_key[rk_idx + 3] ^ X(s1, s2, s3, s0)

            if i + 1 == self.rounds // 2:
                break

            rk_idx += 4
            s0 = self.rd_key[rk_idx + 0] ^ X(d1, d0, d3, d2)
            s1 = self.rd_key[rk_idx + 1] ^ X(d0, d3, d2, d1)
            s2 = self.rd_key[rk_idx + 2] ^ X(d3, d2, d1, d0)
            s3 = self.rd_key[rk_idx + 3] ^ X(d2, d1, d0, d3)

        rk_idx += 4

        out32[0] = ReverseU32(self.rd_key[rk_idx + 0] ^ O(d3, d2, d1, d0))
        out32[1] = ReverseU32(self.rd_key[rk_idx + 1] ^ O(d2, d1, d0, d3))
        out32[2] = ReverseU32(self.rd_key[rk_idx + 2] ^ O(d1, d0, d3, d2))
        out32[3] = ReverseU32(self.rd_key[rk_idx + 3] ^ O(d0, d3, d2, d1))


class AES_DATA(object):
    # 0x178 byte
    _data: byteClass = None
    # D: List[int] = None  # 92 * 4 byte = 368 byte
    # single block function pointer : 4 byte
    # ctx pointer : 4byte
    ctx: AES_CTX = None

    def __init__(self, ctx: AES_CTX = None):
        super(AES_DATA, self).__init__()
        self._data = byteClass.fromhex("00" * 0x170)
        self.ctx = ctx

    def __ne__(self, other):
        if not isinstance(other, AES_DATA):
            return True

        if self._data != other._data:
            return True

        return False

    def __eq__(self, other):
        return not self.__ne__(other)

    @classmethod
    def from_bytes(cls, data: bytes):  # for pytest
        assert len(data) == 0x170
        obj = cls()
        obj._data = byteClass(data)
        return obj

    @classmethod
    def from_hex(cls, data: str, ctx: AES_CTX = None):  # for pytest
        assert len(data) in [0x178 * 2, 0x170 * 2]
        obj = cls().from_bytes(bytes.fromhex(data[:0x170 * 2]))
        obj.ctx = ctx
        return obj

    @property
    def DA1(self):
        return self._data.with_offset_u8(0)

    @property
    def DA4(self):
        return self._data.with_offset_u32(0)

    @property
    def DA8(self):
        return self._data.with_offset_u64(0)

    @property
    def DB1(self):
        return self._data.with_offset_u8(80)

    @property
    def DB4(self):
        return self._data.with_offset_u32(80)

    @property
    def DB8(self):
        return self._data.with_offset_u64(80)

    def clear(self):
        self._data = byteClass(b"\0" * 0x170)

    def initialize(self, ctx: AES_CTX):
        """
            ver 7.9.0 : .text:02424863 ; int __cdecl sub_2424863(AES_DATA *s, ctx, fn)
        """
        self.clear()
        self.ctx = ctx

        self.ctx.single_block_encrypt(self.DB1, self.DB1)

        m21 = ReverseU32(self.DB4[0])
        m20 = ReverseU32(self.DB4[1])
        m23 = ReverseU32(self.DB4[2])
        m22 = ReverseU32(self.DB4[3])

        v6 = self.DB1[15]

        self.DB4[0] = m20
        self.DB4[1] = m21
        self.DB4[2] = m22
        self.DB4[3] = m23

        m10 = u32(__PAIR_R1__(m21, m20))
        m11 = u32(-(v6 & 0x1)) & 0xE1000000 ^ (m21 >> 1)
        m12 = u32(__PAIR_R1__(m23, m22))
        m13 = u32(__PAIR_R1__(m20, m23))

        n20 = u32(__PAIR_R1__(m11, m10))
        n21 = u32(-(m12 & 0x1)) & 0xE1000000 ^ (m11 >> 1)
        n22 = u32(__PAIR_R1__(m13, m12))
        n23 = u32(__PAIR_R1__(m10, m13))

        n10 = u32(__PAIR_R1__(n21, n20))
        n11 = u32(-(n22 & 0x1)) & 0xE1000000 ^ (n21 >> 1)
        n12 = u32(__PAIR_R1__(n23, n22))
        n13 = u32(__PAIR_R1__(n20, n23))

        M = [
            [0, 0, 0, 0],
            [m10, m11, m12, m13],
            [m20, m21, m22, m23],
            [0, 0, 0, 0],
        ]
        N = [
            [0, 0, 0, 0],
            [n10, n11, n12, n13],
            [n20, n21, n22, n23],
            [0, 0, 0, 0],
        ]

        for i in range(4):
            M[3][i] = M[1][i] ^ M[2][i]
            N[3][i] = N[1][i] ^ N[2][i]

        idx = 4
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    self.DB4[idx] = M[i][k] ^ N[j][k]
                    idx += 1

    def set_iv(self, iv: bytePtr):
        """
            ver 7.9.0 : .text:02424CAE ; _DWORD __cdecl aes_hash_with_random(AES_DATA *a1, _BYTE *randomData, _DWORD le
        """
        iv = iv.as_u8
        v5 = 0
        self.DB8[35] = 0
        self.DA8[0] = 0
        self.DA8[1] = 0
        self.DA8[6] = 0
        self.DA8[7] = 0
        self.DA8[8] = 0
        self.DA8[9] = 0

        if len(iv) == 12:
            memcpy(self.DA1, iv, len(iv))
            self.DA1[15] = 1
            v5 = 2
        else:
            assert NotImplementedError("todo")

        self.ctx.single_block_encrypt(self.DA1, self.DA8.offset(4))
        self.DA4[3] = ReverseU32(v5)

        return v5 >> 16

    def _inc_count(self):
        n = ReverseU32(self.DA4[3])
        self.DA4[3] = ReverseU32(n+1)

    def _encode_body_0xC00(self, in_data: bytePtr, out_data: bytePtr, len_data: int):
        offset = 0
        u32in = in_data.as_u32
        u32out = out_data.as_u32

        if len_data < 0xC00:
            return offset

        while len_data - offset > 0xC00:
            pOut = u32out.clone()

            for i in range(192):
                self.ctx.single_block_encrypt(self.DA1, self.DA1.offset(16))
                self._inc_count()
                for j in range(4):
                    pOut[j] = u32in[j] ^ self.DA4[j+4]
                pOut = pOut.byte_offset(16)
                u32in = u32in.byte_offset(16)
                offset += 16

            InvMix_2(self.DB1.byte_offset(16), self.DA1.byte_offset(64), u32out, 0xC00)
            u32out = pOut.clone()

        return offset

    def _encode_body_0x10(self, in_data: bytePtr, out_data: bytePtr, len_data: int):
        offset = 0
        u32in = in_data.as_u32
        u32out = out_data.as_u32
        pOut = out_data.as_u32

        if len_data < 0x10:
            return offset

        while len_data - offset >= 0x10:
            self.ctx.single_block_encrypt(self.DA1, self.DA1.offset(16))
            self._inc_count()

            for j in range(4):
                pOut[j] = u32in[j] ^ self.DA4[j+4]

            pOut = pOut.byte_offset(16)
            u32in = u32in.byte_offset(16)

            offset += 0x10

        InvMix_2(self.DB1.byte_offset(16), self.DA1.byte_offset(64), u32out, len_data & 0xFFFFFFF0)

        return offset

    def _encode_body_0x1(self, in_data: bytePtr, out_data: bytePtr, len_data: int):

        u8in = in_data.as_u8
        u8out = out_data.as_u8

        offset = 0
        if len_data < 1:
            return offset

        self.ctx.single_block_encrypt(self.DA1, self.DA1.offset(16))
        self._inc_count()

        for i in range(len_data):
            u8out[i] = u8in[i] ^ self.DA1[i + 16]
            self.DA1[i + 64] ^= u8out[i]

        return len_data

    def encode_body(self, in_data: bytePtr, out_data: bytePtr, len_data: int):
        """
            ver 7.9.0 : .text:02425277 ; signed int __cdecl aes_encode_body(AES_DATA *a1, _BYTE *a2, _BYTE *a3, _DWORD a4)
        """
        offset = 0
        v5 = len_data + self.DA8[7]
        if v5 > 0xFFFFFFFE0:
            return -1

        self.DA8[7] = v5

        if self.DB4[71]:
            InvMix_1(self.DA1.byte_offset(64), self.DB1.byte_offset(16))
            self.DB4[71] = 0

        if self.DB4[70]:
            return 0

        offset += self._encode_body_0xC00(
            in_data.byte_offset(offset),
            out_data.byte_offset(offset),
            len_data - offset
        )

        # hexdump(out_data._obj._data)

        offset += self._encode_body_0x10(
            in_data.byte_offset(offset),
            out_data.byte_offset(offset),
            len_data - offset
        )
        # hexdump(out_data._obj._data)

        ret = self._encode_body_0x1(
            in_data.byte_offset(offset),
            out_data.byte_offset(offset),
            len_data - offset
        )
        # hexdump(out_data._obj._data)

        self.DB4[70] = ret

        return ret

    def _decode_body_0xC00(self, in_data: bytePtr, out_data: bytePtr, len_data: int):
        offset = 0

        u32in = in_data.as_u32
        u32out = out_data.as_u32

        if len_data < 0xC00:
            return offset

        while len_data - offset > 0xC00:
            InvMix_2(self.DB1.byte_offset(16), self.DA1.byte_offset(64), u32in, 0xC00)
            pOut = u32out.clone()

            for i in range(192):
                self.ctx.single_block_encrypt(self.DA1, self.DA1.byte_offset(16))
                self._inc_count()
                for j in range(4):
                    pOut[j] = u32in[j] ^ self.DA4[j+4]
                pOut = pOut.byte_offset(16)
                u32in = u32in.byte_offset(16)
                offset += 16

            u32out = pOut.clone()
        return offset

    def _decode_body_0x10(self, in_data: bytePtr, out_data: bytePtr, len_data: int):
        offset = 0
        u32in = in_data.as_u32
        pOut = out_data.as_u32

        if len_data < 0x10:
            return offset

        InvMix_2(self.DB1.byte_offset(16), self.DA1.byte_offset(64), u32in, len_data & 0xFFFFFFF0)

        while len_data - offset >= 0x10:
            self.ctx.single_block_encrypt(self.DA1, self.DA1.offset(16))
            self._inc_count()

            for j in range(4):
                pOut[j] = u32in[j] ^ self.DA4[j + 4]

            pOut = pOut.byte_offset(16)
            u32in = u32in.byte_offset(16)

            offset += 0x10

        return offset

    def _decode_body_0x1(self, in_data: bytePtr, out_data: bytePtr, len_data: int):

        u8in = in_data.as_u8
        u8out = out_data.as_u8

        offset = 0
        if len_data < 1:
            return offset

        self.ctx.single_block_encrypt(self.DA1, self.DA1.offset(16))
        self._inc_count()

        for i in range(len_data):
            self.DA1[i + 64] ^= u8in[i]
            u8out[i] = u8in[i] ^ self.DA1[i + 16]

        return len_data

    def decode_body(self, in_data: bytePtr, out_data: bytePtr, len_data: int):
        """
            ver 7.9.0 : .text:02425603 aes_decode_body
        """
        offset = 0
        v5 = len_data + self.DA8[7]
        if v5 > 0xFFFFFFFE0:
            return -1

        self.DA8[7] = v5

        if self.DB4[71]:
            InvMix_1(self.DA1.byte_offset(64), self.DB1.byte_offset(16))
            self.DB4[71] = 0

        if self.DB4[70]:
            return 0

        offset += self._decode_body_0xC00(
            in_data.byte_offset(offset),
            out_data.byte_offset(offset),
            len_data - offset
        )

        # hexdump(out_data._obj._data)

        offset += self._decode_body_0x10(
            in_data.byte_offset(offset),
            out_data.byte_offset(offset),
            len_data - offset
        )
        # hexdump(out_data._obj._data)

        ret = self._decode_body_0x1(
            in_data.byte_offset(offset),
            out_data.byte_offset(offset),
            len_data - offset
        )
        # hexdump(out_data._obj._data)

        self.DB4[70] = ret

        return ret

    def xmm(self, out_data:bytearray):
        aes_xmm(self.DA1.as_u8)

        val = self.DA8.offset(8).as_u128[0]
        out_data[:] = val.to_bytes(16, byteorder='little')


def _convert_to_bytePtr(d):
    if isinstance(d, str):
        return byteClass(d.encode('utf-8')).u8
    elif isinstance(d, (bytes, bytearray)):
        return byteClass(d).u8
    elif isinstance(d, (byteClass)):
        return d.u8
    return d


AesType = Union[str, bytes, bytearray, byteClass, bytePtr]


def ts_aes_encode(key: AesType, iv: AesType, in_body: AesType, out_buff: bytearray, out_dest: bytearray):
    aes_ctx = AES_CTX()
    aes_data = AES_DATA()

    key = _convert_to_bytePtr(key).as_u8
    iv = _convert_to_bytePtr(iv).as_u8
    in_body = _convert_to_bytePtr(in_body).as_u8

    aes_ctx.set_encrypt_key(userKey=key, bits=len(key) * 8)

    aes_data.initialize(aes_ctx)

    aes_data.set_iv(iv=iv)

    len_body = len(in_body)
    buff = byteClass(bytearray([0] * len_body)).u8

    aes_data.encode_body(in_data=in_body, out_data=buff, len_data=len_body)

    aes_data.xmm(out_dest)

    out_buff[:] = buff.data()

    return True


def ts_aes_decode(key: AesType, iv: AesType, in_body: AesType, out_buff: bytearray, out_dest: bytearray):
    aes_ctx = AES_CTX()
    aes_data = AES_DATA()

    key = _convert_to_bytePtr(key).as_u8
    iv = _convert_to_bytePtr(iv).as_u8
    in_body = _convert_to_bytePtr(in_body).as_u8

    aes_ctx.set_encrypt_key(userKey=key, bits=len(key) * 8)

    aes_data.initialize(aes_ctx)

    aes_data.set_iv(iv=iv)

    len_body = len(in_body)
    buff = byteClass(bytearray([0] * len_body)).u8

    aes_data.decode_body(in_data=in_body, out_data=buff, len_data=len_body)

    aes_data.xmm(out_dest)

    out_buff[:] = buff.data()
    return True


def ts_aes_decode_with_tsid(body: Union[bytearray, bytes], ts_id: str) ->bytearray:
    assert len(ts_id) == 3 + 24 + 32
    assert ts_id[:3] == "002"

    key = byteClass(settings.TS_AES_KEY)
    inbody = byteClass(body)
    iv = byteClass(bytearray.fromhex(ts_id[3:3 + 24]))

    # call
    buff = bytearray([])
    dest = bytearray([])

    ts_aes_decode(key=key.u8, iv=iv.u8, in_body=inbody.u8, out_buff=buff, out_dest=dest)

    return buff