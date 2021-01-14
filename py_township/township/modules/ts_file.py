import base64
from pathlib import Path
import random
from typing import Union

import zstd
import zlib
from modules.ts_gzip import ts_uncompress
from modules.ts_utils import u32, u8, u16, RB2, ROL8


def mmh2(data: Union[bytes, bytearray], length: int, seed: int):
    m = 0x5bd1e995
    r = 24
    h = seed ^ length

    i = 0
    while length >= 4:
        k = int.from_bytes(data[i:i+4], byteorder='little', signed=False)

        k = u32(k * m)
        k = u32(k) ^ u32(k >> r)
        k = u32(k * m)

        h = u32(h * m)
        h = u32(h ^ k)

        i += 4
        length -= 4

    if length >= 3:
        h ^= data[i + 2] << 16
    if length >= 2:
        h ^= data[i + 1] << 8
    if length >= 1:
        h ^= data[i + 0]
        h = u32(h * m)

    h ^= h >> 13
    h = u32(h * m)
    h ^= h >> 15

    return u32(h)


def get_hash_table(length: int, seed: int) -> bytearray:
    length = u32(length)
    seed = u32(seed)
    table = bytearray([0] * 0x2d7)

    h = seed
    for i in range(0, 0x2d7, 4):
        v = h.to_bytes(4, 'little')
        h = mmh2(v, 4, length)

        v = h.to_bytes(4, 'little')
        for j in range(0, 4):
            if i + j >= 0x2d7:
                break
            table[i + j] = v[j]

    return table


def get_hash_table2(key: int) -> bytes:
    """
       ver 7.9.0 : .text:00361576 get_hash_table_2 proc near

    Parameters
    ----------
    key

    Returns
    -------

    """
    ret = ''
    if key == 0x41 :
        ret += "AO[hUyI.o|q@p^ Ms1I7 Zub:a'O4Y'_0;XmZ~vK=nJ#wYCccn^CzJu4<f5ogy]}#K5FIlKnnwT_^dVAZgv]D WIt@sl!i=)qxnWh'QuBgR~yZe"
        ret += "oh-cC@q@>6-VvT2,ZSWlU~th+%0|W_iPl}M0un?pydqul`|ZL`u7rm1L0ewz4c9*fnRZF:8(;&%6[Gn>,LXW9F?QQ41(:5svrGV#{'3)]2/6ln["
        ret += "sYds:qTdBh8OyB<#Q!U%Q'[d+r%)OBOuy]!=}ag0GP6Z~`+9>rF&`_8^}N~X02D)H#}aO)08tqx:,O&fNp{R$W>)MBeLi|RX:.z'5B%g]13Ef y"
        ret += "%K?{RApgk{.1),Z]_l,]v~'mrvB)uG.sw2P%Q+|NQL`>IfyLwd],I?f+ig:o8s#LRMy($0Y2VzXBEV~oph4p/dumT(6x{3Q~&mma)%/~BRcnojy"
        ret += "TfT.yqn&sk9j;ay3pg+,ccJG=TEu2K-*d%IU*Y2N).}{UP_N*x?u9fw$Vgj%AtBG+dRE(:n(tI'b47?szaINkm8{<7jL#t;SJ;I'_vrVCoz!E2y"
        ret += "*<n&RjOeoiOE3[?ILO+?dS@u|]vVIHgivtw#_rlogL?rclJkA2V6dH_av 7aSZ6RBgQbL)fW11b<'GW'M)N#ll^qZ{]:baj@nv9YQy`(8'&w_v("
        ret += "PST6KH0OJB04xx>RC3!kRx*|+25^OSh.X'&N>`m9KfIWo|S2jhbc fTd"
    else:
        ret += "BLD18qQhOwEylkVki91hjILTcIwbEMhUHamjkAzgyIWnl1tqOZvO+7AvOTqn036uyHAQVVbSH3/BzYMjNHTMXvogJBWI1siiMZF2zFzD0GEpuGd"
        ret += "F+WbSIrug4fzHojQ/AAaBx2HT/tZ8hP+ITRc8z9a7ecsrGX+EBq+b3mada6zeJPxE2j47psb/J4Xnx0AEfh+lEb2GLpczI7e3o0BGP9GlmQYPSX"
        ret += "INq87N2D8G175+cBwbMmzdfsIxr9hNGJgLGTFe/NdMP6NoAERNJOij9vzbgwiaOpdvmqBkV2HLp//Pj28HgIc392BrzFQ/slGN0/TqxugL1UY9G"
        ret += "MpmI+GQVDSMzswGVWZ5VMjs4sSvkAmQ/p5AnrRyDoszxO+SKI5HV+OwHS0G7NcKXUMCx32xk6mVNxcpl0DwivGhJuvk/gphiG0b2f0gciQaaDJz"
        ret += "uOJASND397ryTg4EuRYRw8D2A1lNF5lGEkzxMCGi56t4zCLduBcROWbbjBKKZer6enhbgsEytVBmzo4ONfQ+ZFv3sLhaEb72lnMkVKDD3tw7hzA"
        ret += "oL86ObHGLOEGMUY3n9wihn1peBNBTcL3kSfH4/t9KF4qZ3GtXA++WO1h5/0edqVhDygXMUzQ87EZvcGuqLMk6iR08pFBO529aAADg8o9hHKfspY"
        ret += "vwghDW/5HtJGL7CrGpE4Sr8FnvNvv7J3AGa9csWrhMB00P/dupnCafDuJAeCgFL0l"

    return ret.encode('ascii')


def _encode_0x79(in_bytearray: bytearray):
    string_length = len(in_bytearray)
    size = string_length

    hash_length = u32((size ^ 0x396A8) + ((string_length+8) ^ 0xC5EED) )
    hash_seed = random.randint(0, 0xFFFFFFFF)

    out_buffer = bytearray([0x79])
    out_buffer[0] = 0x79
    out_buffer += hash_length.to_bytes(length=3, byteorder='little', signed=False)
    out_buffer += hash_seed.to_bytes(length=4, byteorder='little', signed=False)
    out_buffer += in_bytearray

    hashtable = get_hash_table(length=hash_length, seed=hash_seed + 4)

    i = 8
    j = 0

    prev = 0

    for idx in range(string_length):
        curr = out_buffer[i]
        out_buffer[i] ^= hashtable[j]
        out_buffer[i] = u8(prev + out_buffer[i])
        prev = curr
        i += 1
        j = (j+1) % 0x2d7

    return out_buffer


def _decode_0x79(in_bytearray: bytearray, string_length: int):
    """
        .text:01109ACA xml_decode_0x79 proc near

    Parameters
    ----------
    in_bytearray

    out_bytearray

    Returns
    -------

    """
    t = in_bytearray[0]
    assert t == 0x79

    hash_length = int.from_bytes(in_bytearray[1:1+3], byteorder='little', signed=False)
    hash_seed = int.from_bytes(in_bytearray[4:4+4], byteorder='little', signed=False)

    hashtable = get_hash_table(length=hash_length, seed=hash_seed + 4)

    size = u32((hash_length - (string_length ^ 0xC5EED))) ^ 0x396A8

    out_bytearray = in_bytearray[8:]

    i, j = 0, 0
    while i < size:
        if i > 0:
            out_bytearray[i] = u8(out_bytearray[i] - out_bytearray[i-1])
        out_bytearray[i] ^= hashtable[j]

        i += 1
        j = (j + 1) % 0x2d7

    return out_bytearray


def _decode_0x7D(in_bytearray: bytearray):
    key = in_bytearray[0]
    assert key == 0x7D

    hashtable = get_hash_table2(key ^ 0x3C)

    out_bytearray = in_bytearray[:]

    size = len(out_bytearray)
    len_hashtable = len(hashtable)

    i, j = 0, 0
    while i < size:
        out_bytearray[i] ^= hashtable[j]

        i += 1
        j = (j + 1) % len_hashtable
    return out_bytearray


# def _decode_0x50(in_bytearray: bytearray):
#     key = in_bytearray[0]
#     assert key == 0x50
#
#     hashtable = get_hash_table2(key ^ 0x3C)
#
#     out_bytearray = in_bytearray[:]
#
#     size = len(out_bytearray)
#     len_hashtable = len(hashtable)
#
#     i, j = 0, 0
#     while i < size:
#         if i > 0:
#             out_bytearray[i] = u8(out_bytearray[i] - out_bytearray[i - 1])
#         out_bytearray[i] ^= hashtable[j]
#
#         i += 1
#         j = (j + 1) % len_hashtable
#
#     return out_bytearray


def _decode_0x66(in_bytearray: bytearray):
    key = in_bytearray[0]
    assert key == 0x66

    hashtable = get_hash_table2(66)

    out_bytearray = in_bytearray[:]

    size = len(out_bytearray)
    len_hashtable = len(hashtable)

    i, j = 0, 0
    while i < size:
        if i > 0:
            out_bytearray[i] = u8(out_bytearray[i] - out_bytearray[i - 1])

        out_bytearray[i] ^= hashtable[j]

        i += 1
        j = (j + 1) % len_hashtable
    return out_bytearray


def _decode_0xAD(in_bytearray: bytearray):
    key = in_bytearray[0]
    assert key == 0x6f

    hashtable = get_hash_table2(88)

    out_bytearray = in_bytearray[:]

    size = len(out_bytearray)
    len_hashtable = len(hashtable)

    i, j = 0, 0
    while i < size:
        if i > 0:
            out_bytearray[i] = u8(out_bytearray[i] - out_bytearray[i - 1])

        out_bytearray[i] ^= hashtable[j]

        i += 1
        j = (j + 1) % len_hashtable
    return out_bytearray


def _deocode_xor(in_bytearray: bytearray) -> bytearray:
    """
    .text:01F0474E ; unsigned int __cdecl xml_xor(xmldata *a1, int bDecode, unsigned int offset, char *pEncodedXml, int length)

    Parameters
    ----------
    in_bytearray

    Returns
    -------

    """
    key_hex = "ca656f74c492d5544b861925a915de6786b7b169af25e22774d39c32d0413c8d39f5b8a77bed3c96a308fb8d7b197b2dbf7e002d845d387215b0ef9fe85abfd8"
    key = bytes.fromhex(key_hex)
    len_key = len(key)

    len_in = len(in_bytearray)

    H32 = 0
    R8 = 0
    out = bytearray([0] * len_in)
    for i in range(len_in):
        k = key[i % len_key]
        c = in_bytearray[i]

        new_val = R8 ^ k ^ c ^ u8(H32) ^ RB2(H32) ^ (u16(H32 ^ (H32 >> 16)) >> 8)
        new_val = u8(new_val)
        out[i] = new_val
        R8 = new_val ^ ROL8(R8, 1)
        H32 = u32(H32 + 0x17)

    return out


def _decode_zstd(in_bytearray: bytearray) -> bytearray:
    dctx = zstd.ZstdDecompressor()
    ret = dctx.decompress(in_bytearray)
    return ret

def _decode_45584c50_case7(in_bytearray: bytearray) -> bytearray:
    pass

def _decode_45584c50(in_bytearray: bytearray) -> bytearray:
    """

        ver 7.9.0 : .text:01F00BC4 ; _BOOL4 __cdecl xml_decode_45584c50(_DWORD *a1, XmlFile *a2, int a3, XmlStatus *a4)
        ver 7.9.5 : .text:01F9F564

    Parameters
    ----------
    in_bytearray

    Returns
    -------

    """

    offset = 0
    read_len = 4
    len_data = len(in_bytearray)

    # todo
    # base64 decode
    # base
    while offset < len_data:
        data = int.from_bytes(in_bytearray[offset:offset+read_len], byteorder='little', signed=False)

        if data == 0x1A4B4C42 or data == 0x45584C50:
            offset += 4
            read_len = 4
            continue
        elif u16(data) == 1:
            offset += 4
            j = u16(data >> 16)
            offset += j  # fixme : check.
            return _deocode_xor(in_bytearray=in_bytearray[offset:])

        elif u16(data) == 2:
            raise NotImplementedError('Not Implemented for case 2')
        elif u16(data) == 3:
            offset += 4
            j = u16(data >> 16)
            offset += j
            key = "QTZmZTNGODQ1ODRkNTRsN0EyNjRBZjM5MTU3c0Y4NnU="
            decoded_key = base64.standard_b64decode(key)
            raise NotImplementedError('Not Implemented for case 3')

        elif u16(data) == 4:
            offset += 4
            j = u16(data >> 16)
            offset += j
            return _decode_zstd(in_bytearray=in_bytearray[offset:])
        elif u16(data) == 5:
            raise NotImplementedError('Not Implemented for case 5')
        elif u16(data) == 6:
            raise NotImplementedError('Not Implemented for case 6')
        elif u16(data) == 7:
            # 0700 0e00 02f1 ca06 0000 79a1 e80f a802 e757 d6b9 81c3 039d 0899 dbbd fe3e 5e05 e6cd b669 34e8 8bfc 28e9 ff05

            offset += 4
            # 02f1 ca06 0000 79a1 e80f a802 e757 d6b9 81c3 039d 0899 dbbd fe3e 5e05 e6cd b669 34e8 8bfc 28e9 ff05
            # j = u16(data >> 16)
            # offset += j
            length_offset = offset + 6 + 1
            length = int.from_bytes(in_bytearray[length_offset: length_offset+3], byteorder='little')

            seed_offset = length_offset + 3
            seed = int.from_bytes(in_bytearray[seed_offset:seed_offset+4], byteorder='little')
            hash_table = get_hash_table(length, seed+4)
            buff = in_bytearray[seed_offset+4:]

            j = 0
            for i in range(len(buff)):
                if i > 0:
                    buff[i] = u8(buff[i] - buff[i-1])
                buff[i] ^= hash_table[j]
                j = (j + 1) % 0x2d7


            # 02f1 ca06 0000 79a1 e80f a802 e757 d6b9 81c3 039d 0899 dbbd fe3e 5e05 e6cd b669 34e8 8bfc 28e9 ff05
            return zlib.decompress(buff, wbits=-zlib.MAX_WBITS|16)
        else:
            raise Exception('Unknown data')

    return in_bytearray

key_0x54 = bytes.fromhex("775F7628505354364B48304F4A42303478783E524333216B52782A7C2B32355E4F53682E5827264E3E606D394B6649576F7C53326A686263206654643761535A3652426751624C2966573131623C274757274D294E236C6C5E715A7B5D3A62616A406E763959517960283827264532792A3C6E26526A4F656F694F45335B3F494C4F2B3F645340757C5D765649486769767477235F726C6F674C3F72636C4A6B4132563664485F617620753966772456676A25417442472B645245283A6E287449276234373F737A61494E6B6D387B3C376A4C23743B534A3B49275F767256436F7A216F706834702F64756D542836787B33517E266D6D6129252F7E4252636E6F6A795466542E79716E26736B396A3B61793370672B2C63634A473D544575324B2D2A642549552A59324E292E7D7B55505F4E2A783F5A5D5F6C2C5D767E276D7276422975472E7377325025512B7C4E514C603E4966794C77645D2C493F662B69673A6F3873234C524D792824305932567A584245567E51754267527E795A656F682D63434071403E362D567654322C5A53576C557E74682B25307C575F69506C7D4D30756E3F70796471756C607C5A4C607537726D314C3065777A3463392A666E525A463A38283B2625365B476E3E2C4C585739463F51513431283A357376724756237B2733295D322F366C6E5B735964733A7154644268384F79423C235121552551275B642B7225294F424F75795D213D7D6167304750365A7E602B393E724626605F385E7D4E7E583032442948237D614F2930387471783A2C4F26664E707B5224573E294D42654C697C52583A2E7A27354225675D313345662079254B3F7B524170676B7B2E31292C414F5B685579492E6F7C7140705E204D73314937205A75623A61274F3459275F303B586D5A7E764B3D6E4A2377594363636E5E437A4A75343C66356F67795D7D234B3546496C4B6E6E77545F5E6456415A67765D442057497440736C21693D2971786E5768")


def _encode_x54(in_bytearray: bytearray, encode_bytes = 279) -> bytearray:
    len_key = len(key_0x54)

    len_indata = min( encode_bytes, len(in_bytearray) + 3)

    pData = in_bytearray[:]

    for i in range(len_indata):
        pData[i] ^= key_0x54[i % len_key]
        if i > 0:
            pData[i] = u8(pData[i] + in_bytearray[i - 1])

    pData[0] = u8(pData[0] + 0x54)
    pData[0:0] = bytearray([
        0x54,
        u8((len_indata)) ^ key_0x54[0],
        u8((len_indata) >> 8)
    ])


    return pData


def _decode_x54(in_bytearray: bytearray, len_indata: int) -> bytearray:
    """
        .text:110A33A fetch_city_response_data_decode

    Parameters
    ----------
    in_bytearray

    Returns
    -------

    """
    len_key = len(key_0x54)

    v10 = (in_bytearray[1] ^ key_0x54[0]) | (in_bytearray[2] << 8)
    len_indata = min(v10, len_indata - 3)

    if len_indata == 3:
        pData = in_bytearray[3:3+3]
    else:
        pData = in_bytearray[3:]

    pData[0] = u8(pData[0] - 0x54)

    for i in range(len_indata):
        if i > 0:
            pData[i] = u8(pData[i] - pData[i - 1])
        pData[i] ^= key_0x54[i % len_key]


    return pData


def _decode_x53(in_bytearray: bytearray, len_indata: int) -> bytearray:
    """
        .text:110A33A fetch_city_response_data_decode

    Parameters
    ----------
    in_bytearray

    Returns
    -------

    """
    assert in_bytearray[0] == 0x53

    key = get_hash_table2(66)
    len_key = len(key)

    v10 = (in_bytearray[1] ^ 0x53) | (in_bytearray[2] << 8)

    len_indata = min(v10, len_indata - 3)

    if len_indata == 3:
        pData = in_bytearray[3:3+3]
    else:
        pData = in_bytearray[3:]

    pData[0] = u8(pData[0] - 0x54)

    for i in range(len_indata):
        if i > 0:
            pData[i] = u8(pData[i] - pData[i - 1])
        pData[i] ^= key[i % len_key]

    return pData


def ts_decode_bytearray(in_bytearray: bytearray, string_length: int) -> bytearray:
    """
    ver 7.9.0 : .text:01109CF7 sub_1109CF7

    Parameters
    ----------
    in_bytearray
        encoded content

    string_length
        length of content

    Returns
        decoded content
    -------

    """
    x = in_bytearray[0] ^ 0x3C

    if in_bytearray[0] == 0x54 and x == 0x68:
        return _decode_x54(in_bytearray=in_bytearray, len_indata=string_length)

    elif in_bytearray[0] == 0x53 and x == 0x6F:
        return _decode_x53(in_bytearray=in_bytearray, len_indata=string_length)

    elif in_bytearray[0] == 0x78 and x == 0x44:
        # .text:01109769 sub_1109769
        raise NotImplementedError()
    elif in_bytearray[0] == 0x79 and x == 0x45:
        return _decode_0x79(in_bytearray=in_bytearray, string_length=string_length)

    elif in_bytearray[0] == 0x64 and x == 0x58:
        raise NotImplementedError('Need to check')

    elif in_bytearray[0] == 0x7D and x == 0x41:
        return _decode_0x7D(in_bytearray=in_bytearray)

    elif in_bytearray[0] == 0x66 and x == 0x5A:
        raise NotImplementedError('Need to check')
        # return _decode_0x66(in_bytearray=in_bytearray)

    elif in_bytearray[0] == 0x6F and x == 0x53:
        raise NotImplementedError('Need to check')
        # return _decode_0xAD(in_bytearray=in_bytearray)

    elif in_bytearray[0] == 0x1F and in_bytearray[1] == 0x8B:  # gzip
        return bytearray(ts_uncompress(in_bytearray))

    elif in_bytearray[0] == 0x3C and x == 0x00:  # '<'
        return in_bytearray[:]

    elif in_bytearray[0] == 0x7b and in_bytearray[-1] == 0x7d: # '{' ~ '}'
        return in_bytearray

    elif in_bytearray[0] == 0x50 and in_bytearray[1] == 0x4c and in_bytearray[2] == 0x58 and in_bytearray[3] == 0x45:
        return _decode_45584c50(in_bytearray=in_bytearray)
    else:
        raise Exception('unknown data')


def ts_decode_file(in_filename: Path, out_filename: Path):
    in_buffer = bytearray(in_filename.read_bytes())
    len_buffer = len(in_buffer)

    out_buffer = ts_decode_bytearray(in_bytearray=in_buffer, string_length=len_buffer)

    while out_buffer[-1] == 0x00:
        del out_buffer[-1]
    out_filename.write_bytes(out_buffer)
