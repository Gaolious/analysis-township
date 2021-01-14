import pytest

from app_root.keywords.utils import decode_keyword


@pytest.mark.parametrize("input, output", [
    (b"\x2F\x2A\x0C\x00\x03\xE1\xDF\xE8\xCC\xD3\xDE\xC6", "bronzePrice")
])
def test_decode_keyword(input, output):

    ret = decode_keyword(input)

    assert ret == output


