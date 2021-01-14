from modules.ts_utils import u8


def decode_keyword(encoded_string: bytearray) -> str:
    """
        ver 7.9.0 : .text:020566D7
    Parameters
    ----------
    encoded_string

    Returns
    -------

    """

    length = len(encoded_string) - 1
    ret = bytearray([0] * length)

    s = encoded_string[length]

    s = u8(s - length*length)

    for i in range(length):
        ret[i] = u8(s ^ encoded_string[i])
        s = u8(s + length)

    return ret.decode('utf-8')
