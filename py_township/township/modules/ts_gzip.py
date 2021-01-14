
import zlib


ZLIB_COMPRESS_LEVEL = 8
ZLIB_MEMORY_LEVEL = 8
ZLIB_WBITS = 31


def ts_compress(data) -> bytearray:
    if isinstance(data, str):
        data = data.encode('utf-8')

    deflate = zlib.compressobj(
        level=ZLIB_COMPRESS_LEVEL,
        method=zlib.DEFLATED,
        wbits=ZLIB_WBITS,
        memLevel=ZLIB_MEMORY_LEVEL,
        strategy=zlib.Z_DEFAULT_STRATEGY,
    )
    ret = bytearray(deflate.compress(data) + deflate.flush())
    # fake
    return ret


def ts_uncompress(data) -> bytearray:
    inflate = zlib.decompressobj(ZLIB_WBITS)
    ret = bytearray(inflate.decompress(data) + inflate.flush())
    return ret


def ts_decompress(data) -> bytearray:
    return ts_uncompress(data)

