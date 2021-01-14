import base64
import json
from pathlib import Path

from modules.ts_aes import ts_aes_decode, ts_aes_decode_with_tsid
from modules.ts_file import ts_decode_bytearray, ts_decode_file, _encode_0x79, _decode_0x79
from modules.ts_gzip import ts_uncompress


def parse_request_data(base_path : Path):
    body_file = base_path / "body.txt"
    ts_id_file = base_path / "header.txt"

    out_decoded_body_file = base_path / "decodd_body.txt"
    out_data_body_file = base_path / "decodd_data.txt"

    body = bytearray.fromhex(body_file.read_bytes().decode('utf-8'))
    ts_id = ts_id_file.read_bytes().decode('utf-8')

    decoded_body = ts_aes_decode_with_tsid(body=body, ts_id=ts_id)
    uncompress_body = ts_uncompress(decoded_body)
    out_decoded_body_file.write_bytes(uncompress_body)

    json_body = json.loads(uncompress_body.decode('utf-8'))
    data = json_body['data']

    if data:
        data = bytearray(base64.b64decode(data))

        decode_data = ts_decode_bytearray(data, len(data))

        # tmp_encode = _encode_0x79(decode_data)
        # decode2_data = _decode_0x79(tmp_encode, len(tmp_encode))

        uncompressed_data = ts_uncompress(decode_data)
        out_data_body_file.write_bytes(uncompressed_data)


def test():
    # bytearray(b'{"add":0,"ch":false,"cityId":"yUAemuNvdz","eventId":370,"jb":true,"myscores":90 }')
    body = bytearray.fromhex("4f076a0349ed66a8c1d0bdcb5a69c2bf3f3c5dbeb2ebe1de928f4d2c945dbdc4115d05d099d8ad1d6954b26366f2ce66830537a3d3e0e53c81c7fbb5eea6cd455f860bec08529a8f0cb25ef7f368ab1019e254eac1b19febf83fa31e5aa8")
    ts_id = "002b8742504b60d1cf37fa19cdae1d07c2d40ba1475ad5fb29e86ed29f8"
    decoded_body = ts_aes_decode_with_tsid(body=body, ts_id=ts_id)
    uncompress_body = ts_uncompress(decoded_body)
    # body_file = Path("D:/github/analysis-township/py_township/ts_log/accounts/7.9.5/gaolious1/20201229/save_city_body.txt")
    # header = Path("D:/github/analysis-township/py_township/ts_log/accounts/7.9.5/gaolious1/20201229/save_city_header.txt")
    #
    # out_decoded_body_file = Path("D:/github/analysis-township/py_township/ts_log/accounts/7.9.5/gaolious1/20201229/decode_save_city_body.txt")
    #
    # body = body_file.read_bytes()
    # ts_id = json.loads(header.read_bytes().decode('utf-8'))['ts-id']
    #
    #
    # decoded_body = ts_aes_decode_with_tsid(body=body, ts_id=ts_id)
    # uncompress_body = ts_uncompress(decoded_body)
    # out_decoded_body_file.write_bytes(uncompress_body)


    # base_path = Path("D:/playrix/Log/saved/1")
    #
    # parse_request_data(base_path=base_path)
    #
    # base_path = Path("D:/playrix/Log/compare/saves")
    base_path = Path("D:/playrix/Log/saved/1")

    in_global_vars = base_path / "GlobalVars.xml"
    out_global_vars = base_path / "out_GlobalVars.xml"

    in_local_info = base_path / "LocalInfo.xml"
    out_local_info = base_path / "out_LocalInfo.xml"

    in_mGameInfo = base_path / "mGameInfo.xml"
    out_mGameInfo = base_path / "out_mGameInfo.xml"
    new_mGameInfo = base_path / "new_mGameInfo.xml"

    # ts_decode_file(in_global_vars, out_global_vars)
    # ts_decode_file(in_local_info, out_local_info)
    if not out_mGameInfo.exists():
        ts_decode_file(in_mGameInfo, out_mGameInfo)

    if not new_mGameInfo.exists():
        """
    		<Var name="WareHouseCashUpgrade" v="1" t="i"/>
        
        """
        new_mGameInfo.write_bytes(
            _encode_0x79(
                bytearray(out_mGameInfo.read_bytes())
            )
        )


def run():
    hex_string = "062a687a0e98216061d6f029b2a3be1c9434135471d011d354a42299864461b699a53db7c7a65bd387e15a3d2cdc86448dbbae01993d6d2615063878f8d4a6a900a2230767650b4a6de12672d11281f883918b0d56b0ef6cf5b05976213b22e37a5b1f11bf787fca2415537ffb17e9e4221ae176403601437ad5d428d92f3044dd21fdc7afc7879aa93b38656040c98c6a6c0b568181bc273bf28974131c2ed66cfb0e9c650c4f6c740b8589f9d4b7bdd3502f4eca78b9f9f2395c59ffa3ccfbdff142a83bb4ecdd55d08d4e85cc8a9c0a4a5be684c4f9a4333a77ae6f00e459e65756ce162c92d96e774cd7c23dc5f4a8806052769faf9e78230794536c99454833471e2eb72014fb009a8f47b88b26b8af036cee26d110c7353b8c60a928835a1ecdec6b25c68bd3b3faf2b24625d53da4d1a3b1d3dbafa80a24dfc16c5ee6344e04503bf4dc010a2cff7a7eebee0f3fc4a5cc9c28e8c8d1ab5b13bbdb0b8850c67760bec1b68150ef368975e73861679219749ad50ac64dd658ae93a2a8bc6a9b16511be63224f370f3c70215f3bcec4450c60145c8ff0fa7de6db9da00a3a2f6ee8c405816670ad7554af0794394129c6b35d0c28cbacd4272a9fd69ddefcf12981dc1febc3ca221d59c7f23e2e9d2c384f130cda48cb431f7b538f94bfd7d2afde631b7b96a11a72cf0a93e50fe2f6f06945b50abdafd84c386d8fea7dd2712caafba4195465f2c3238173f86b66d8a9891b5a76226aeda579db51c616fab9d65cb74d5820f0aadf6655b735b987ac39b1aaed897e50f222a15d3f0f5153626074f63caeeafa08fa6acc713a6a19f2d923ea2b9fea6fca819a3b7f717ab989afc019cb3d377f8973bfc628ea65dd143a9fee5bd4cda8f40a24b8eca0ef8202792c36ce8535bfcfc5d20bd16"
    ts_id = "002045266fe95ec9f413f99b502f25c88dd509c1824a868e10183eb9d6e"

    hex_string = "af5fe5efd54f2b874aeea756114e0cdca8e00e70fa34109db4e444a2f9151e462c8f2545f2229759759afd461ea42713e8393ef17bb01818"
    ts_id = "00283efe115fb584b7c8131ea40529e7c98bd51cb596ce676d6b9a59455"
    data = bytearray.fromhex(hex_string)

    ret = ts_aes_decode_with_tsid(data, ts_id)
    ret = ts_uncompress(ret)
    pass