import pytest
from django.conf import settings

from modules.tests.test_aes_data import data_decode, data_AES_DATA_encode, data_encode, data_InvMix_2, data_InvMix_1, \
    data_AES_DATA_set_iv, data_AES_DATA_initialize, data_AES_CTX_single_block_encrypt, data_AES_CTX_set_encrypt_key
from modules.ts_aes import AES_CTX, AES_DATA, InvMix_1, InvMix_2, ts_aes_decode, ts_aes_encode
from modules.ts_bytes import byteClass
from modules.ts_gzip import ts_decompress


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_AES_CTX_set_encrypt_key))])
def test_AES_CTX_set_encrypt_key(idx):
    bits, in_ctx_data, ret, out_ctx_data = data_AES_CTX_set_encrypt_key[idx]

    key = byteClass(settings.TS_AES_KEY).u8

    # prepare
    in_ctx = AES_CTX.from_hex(in_ctx_data)
    out_ctx = AES_CTX.from_hex(out_ctx_data)

    # call
    in_ctx.set_encrypt_key(userKey=key, bits=bits)

    # check
    assert in_ctx == out_ctx


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_AES_CTX_single_block_encrypt))])
def test_AES_CTX_single_block_encrypt(idx):
    in_p1, in_rd_key, out_p1, out_rd_key = data_AES_CTX_single_block_encrypt[idx]

    in_p1 = byteClass.fromhex(in_p1)
    out_p1 = byteClass.fromhex(out_p1)

    # prepare
    in_ctx = AES_CTX.from_hex(in_rd_key)
    out_ctx = AES_CTX.from_hex(out_rd_key)

    # call
    in_ctx.single_block_encrypt(in_p1.u8, in_p1.u8)

    assert in_p1 == out_p1
    assert in_ctx == out_ctx


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_AES_DATA_initialize))])
def test_AES_DATA_initialize(idx):
    in_aes_data, in_aes_ctx, out_aes_data, out_aes_ctx = data_AES_DATA_initialize[idx]

    in_ctx = AES_CTX.from_hex(in_aes_ctx)
    in_data = AES_DATA.from_hex(in_aes_data)

    out_ctx = AES_CTX.from_hex(out_aes_ctx)
    out_data = AES_DATA.from_hex(out_aes_data)

    in_data.initialize(in_ctx)

    assert in_ctx == out_ctx
    assert in_data == out_data


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_AES_DATA_set_iv))])
def test_AES_DATA_set_iv(idx):
    in_aes_data, in_aes_ctx, random_data, len, out_ret, out_aes_data, out_ctx = data_AES_DATA_set_iv[idx]

    in_ctx = AES_CTX.from_hex(in_aes_ctx)
    in_data = AES_DATA.from_hex(in_aes_data, in_ctx)

    out_ctx = AES_CTX.from_hex(out_ctx)
    out_data = AES_DATA.from_hex(out_aes_data, out_ctx)

    iv = byteClass.fromhex(random_data)

    in_data.set_iv(iv.u8)

    assert in_ctx == out_ctx
    assert in_data == out_data


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_InvMix_1))])
def test_InvMix_1(idx):
    in_data, out_data = data_InvMix_1[idx]

    in_data = byteClass.fromhex(in_data)
    out_data = byteClass.fromhex(out_data)

    InvMix_1(in_data.with_offset_u8(0), in_data.with_offset_u8(0x20))

    assert in_data == out_data


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_InvMix_2))])
def test_InvMix_2(idx):
    in_p1, in_2p, in_p3, in_p4, out_p2, out_p3 = data_InvMix_2[idx]

    in_p1 = byteClass.fromhex(in_p1)
    in_p2 = byteClass.fromhex(in_2p)
    in_p3 = byteClass.fromhex(in_p3)
    cnt = in_p4
    out_p2 = byteClass.fromhex(out_p2)
    out_p3 = byteClass.fromhex(out_p3)

    InvMix_2(in_p1.u8, in_p2.u8, in_p3, cnt)

    assert in_p2 == out_p2
    assert in_p3 == out_p3


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_AES_DATA_encode))])
def test_data_AES_DATA_encode(idx):
    in_aes_data, in_aes_ctx, in_body, in_len, out_aes_data, out_aes_ctx, out_buff = data_AES_DATA_encode[idx]

    in_ctx = AES_CTX.from_hex(in_aes_ctx)
    in_data = AES_DATA.from_hex(in_aes_data, in_ctx)

    in_body = byteClass.fromhex(in_body)
    in_buff = byteClass.fromhex("00" * in_len)

    out_ctx = AES_CTX.from_hex(out_aes_ctx)
    out_data = AES_DATA.from_hex(out_aes_data, out_ctx)
    out_buff = byteClass.fromhex(out_buff)

    in_data.encode_body(in_body.u8, in_buff.u8, in_len)

    if in_data != out_data:
        a = in_data._data.u8
        b = out_data._data.u8
        for i in range(len(a)):
            if a[i] != b[i]:
                print(i)

    assert in_data == out_data
    assert in_ctx == out_ctx
    assert in_buff == out_buff


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_encode))])
def test_encode(idx):
    len_iv = 0x0c
    len_dest = 0x10

    # prepare
    key = byteClass(settings.TS_AES_KEY)

    iv, in_body, out_body, out_dest = data_encode[idx]

    iv = byteClass.fromhex(iv)
    in_body = byteClass.fromhex(in_body)
    out_body = byteClass.fromhex(out_body)
    out_dest = byteClass.fromhex(out_dest)

    buff = bytearray()
    dest = bytearray()
    ts_aes_encode(key=key.u8, iv=iv.u8, in_body=in_body.u8, out_buff=buff, out_dest=dest)

    assert out_body.data() == buff
    assert out_dest.data() == dest


@pytest.mark.parametrize("idx", [_ for _ in range(len(data_decode))])
def test_decode(idx):
    len_iv = 0x0c
    len_dest = 0x10

    # prepare
    key = byteClass(settings.TS_AES_KEY)

    ts_id, inbody, length, outbody = data_decode[idx]

    ts_id = bytearray.fromhex(ts_id[3:])
    inbody = byteClass.fromhex(inbody)
    offset = 0
    iv = byteClass(ts_id[ offset : offset + len_iv])
    offset += len_iv
    dest = byteClass(ts_id[offset : offset + len_dest])
    outbody = bytearray.fromhex(outbody)

    # call
    buff = bytearray([])
    dest = bytearray([])
    ts_aes_decode(key=key.u8, iv=iv.u8, in_body=inbody.u8, out_buff=buff, out_dest=dest)

    if outbody != buff:
        print(ts_decompress(buff))
    assert outbody == buff

