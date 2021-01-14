import pytest

from modules.tests.test_file_data_decode_0x54 import data_decode_0x54
from modules.tests.test_file_data_decode_0x79 import data_decode_0x79
from modules.tests.test_file_data_decode_0x7D import data_decode_0x7D
from modules.tests.test_file_data_hashtable import data_get_hash_table
from modules.ts_file import mmh2, get_hash_table, _decode_0x79, _decode_0x7D, _decode_x54, _encode_x54
from modules.ts_gzip import ts_uncompress


@pytest.mark.parametrize("data, seed, ret", [
        (bytearray([0x17, 0xA9, 0x50, 0xCC]), 0x000A21E7, 0x4F1CF5A4),
        (bytearray([0xA4, 0xF5, 0x1C, 0x4F]), 0x000A21E7, 0x0D309935),
        (bytearray([0x35, 0x99, 0x30, 0x0D]), 0x000A21E7, 0x0303AF65),
        (bytearray([0x65, 0xAF, 0x03, 0x03]), 0x000A21E7, 0xB21D62F4),
        (bytearray([0xF4, 0x62, 0x1D, 0xB2]), 0x000A21E7, 0x644F8840),
        (bytearray([0x40, 0x88, 0x4F, 0x64]), 0x000A21E7, 0xBDB9FC4F),
        (bytearray([0x4F, 0xFC, 0xB9, 0xBD]), 0x000A21E7, 0xE8CC15A6),
        (bytearray([0xA6, 0x15, 0xCC, 0xE8]), 0x000A21E7, 0xB6F532DC),
        (bytearray([0xDC, 0x32, 0xF5, 0xB6]), 0x000A21E7, 0xB03D1B5C),
        (bytearray([0x5C, 0x1B, 0x3D, 0xB0]), 0x000A21E7, 0x16540DE0),
        (bytearray([0xE0, 0x0D, 0x54, 0x16]), 0x000A21E7, 0xB5520DC2),
        (bytearray([0xC2, 0x0D, 0x52, 0xB5]), 0x000A21E7, 0x7F933CD9),
        (bytearray([0xD9, 0x3C, 0x93, 0x7F]), 0x000A21E7, 0xE972D2A5),
        (bytearray([0xA5, 0xD2, 0x72, 0xE9]), 0x000A21E7, 0xA2A6465F),
        (bytearray([0x5F, 0x46, 0xA6, 0xA2]), 0x000A21E7, 0x4CE443B9),
        (bytearray([0xB9, 0x43, 0xE4, 0x4C]), 0x000A21E7, 0x6429FB44),
        (bytearray([0x44, 0xFB, 0x29, 0x64]), 0x000A21E7, 0xB9F78FCE),
        (bytearray([0xCE, 0x8F, 0xF7, 0xB9]), 0x000A21E7, 0x86B45C50),
        (bytearray([0x50, 0x5C, 0xB4, 0x86]), 0x000A21E7, 0x450420F3),
        (bytearray([0xF3, 0x20, 0x04, 0x45]), 0x000A21E7, 0xF96FEB3B),
        (bytearray([0x3B, 0xEB, 0x6F, 0xF9]), 0x000A21E7, 0x0E01B7DA),
        (bytearray([0xDA, 0xB7, 0x01, 0x0E]), 0x000A21E7, 0x6224B380),
        (bytearray([0x80, 0xB3, 0x24, 0x62]), 0x000A21E7, 0xD3321866),
        (bytearray([0x66, 0x18, 0x32, 0xD3]), 0x000A21E7, 0x851A6B32),
        (bytearray([0x32, 0x6B, 0x1A, 0x85]), 0x000A21E7, 0xD7D82CDD),
        (bytearray([0xDD, 0x2C, 0xD8, 0xD7]), 0x000A21E7, 0xE0B78294),
        (bytearray([0x94, 0x82, 0xB7, 0xE0]), 0x000A21E7, 0xB8F29424),
        (bytearray([0x24, 0x94, 0xF2, 0xB8]), 0x000A21E7, 0x3931D8A8),
    ]
)
def test_mmh2(data, seed, ret):
    assert mmh2(data=data, length=len(data), seed=seed) == ret


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_get_hash_table))])
def test_get_hash_table(idx):
    length, seed, ret = data_get_hash_table[idx]

    ret = bytearray.fromhex(ret)
    val = get_hash_table(length=length, seed=seed)
    assert val == ret



@pytest.mark.parametrize("idx", [_ for _ in range(len(data_decode_0x79))])
def test_decode_0x79(idx):

    in_data, out_data = data_decode_0x79[idx]

    in_data = bytearray.fromhex(in_data)
    out_data = bytearray.fromhex(out_data)
    length = len(in_data)
    if length > 0 and in_data[length - 1] == 0x00:
        length -= 1

    buff = _decode_0x79(in_data, length)

    assert buff == out_data


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_decode_0x7D))])
def test_decode_0x7D(idx):

    in_data, out_data = data_decode_0x7D[idx]

    in_data = bytearray.fromhex(in_data)
    out_data = bytearray.fromhex(out_data)

    length = len(in_data)
    if length > 0 and in_data[length - 1 ] == 0x00:
        length -= 1

    buff = _decode_0x7D(in_data)

    assert buff == out_data

@pytest.mark.parametrize("idx", [_ for _ in range(len(data_decode_0x54))])
def test_decode_0x54(idx):

    _, in_data, out_data = data_decode_0x54[idx]

    in_data = bytearray.fromhex(in_data)
    out_data = bytearray.fromhex(out_data)

    length = len(in_data)
    if length > 0 and in_data[length - 1 ] == 0x00:
        length -= 1

    buff = _decode_x54(in_data, len(in_data))

    assert buff == out_data


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_decode_0x54))])
def test_encode_0x54(idx):
    encode_bytes, out_data, in_data = data_decode_0x54[idx]

    in_data = bytearray.fromhex(in_data)
    out_data = bytearray.fromhex(out_data)

    length = len(in_data)
    if length > 0 and in_data[length - 1] == 0x00:
        length -= 1

    buff = _encode_x54(in_data, encode_bytes)

    assert buff == out_data
