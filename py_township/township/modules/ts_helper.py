import base64
import json
import shutil
import zipfile
from hashlib import md5
from pathlib import Path
import random
from time import sleep
from typing import Any, Dict
from xml.etree import ElementTree

from django.conf import settings

from modules.ts_aes import ts_aes_encode, ts_aes_decode_with_tsid
from modules.ts_file import ts_decode_file, ts_decode_bytearray, _encode_x54
from modules.ts_gzip import ts_compress, ts_uncompress
from modules.ts_request import TsRequest
from core.utils import Logger
from modules.ts_utils import datetime_to_timestamp

log = Logger('default')


class TsFlow(object):
    # config 관련 Path
    contents_path: Path = None           # 계정 무관 컨텐츠
    account_path: Path = None            # 계정 Path
    account_daily_log_path: Path = None  # 계정 일일 단위 로그 Path

    # Fetch city 관련 Path
    fetch_city_header: Path = None  # FetchCity 요청 후 Response의 Header 저장
    fetch_city_body: Path = None  # FetchCity 요청 후 Response의 body 저장
    fetch_city_decode: Path = None  # fetch_city_body decode 내용 저장 (json)
    fetch_city_data_decode: Path = None  # fetch_city_decode의 data항목 decode (xml)

    save_city_data: Path = None
    save_city_resp_header: Path = None
    save_city_resp_body: Path = None

    ts_request: TsRequest = None
    now = None

    city_ver: int = None
    city_id: str = None
    ts_token: str = None
    name: str = None
    deviceId: str = None

    def __init__(self, contents_path:Path, account_path:Path, now):
        self.contents_path = contents_path
        self.account_path = account_path
        self.account_daily_log_path = account_path / now.strftime('%Y%m%d')
        self.ts_request = TsRequest(account_path)
        self.now = now

        str_time = self.now.strftime('%Y%m%d_%H%M%S')
        # str_time = self.now.strftime('%Y%m%d_%H%M')
        self.fetch_city_header = self.account_daily_log_path / "{}_FetchCity_header.log".format(str_time)
        self.fetch_city_body = self.account_daily_log_path / "{}_FetchCity_body.log".format(str_time)
        self.fetch_city_decode = self.account_daily_log_path / "{}_FetchCity_decode.json".format(str_time)
        self.fetch_city_data_decode = self.account_daily_log_path / "{}_FetchCity_data_decode.xml".format(str_time)

        self.save_city_data = self.account_daily_log_path / "{}_SaveCity_body.xml".format(str_time)
        self.save_city_resp_header = self.account_daily_log_path / "{}_SaveCity_resp_header.xml".format(str_time)
        self.save_city_resp_body = self.account_daily_log_path / "{}_SaveCity_resp_body.xml".format(str_time)

    def load_account_config(self):
        path = self.account_path / "account_info.json"
        assert path.exists()

        account_info = json.loads(path.read_bytes())

        self.city_ver = account_info.get('city_ver')
        self.city_id = account_info.get('city_id')
        self.ts_token = account_info.get('ts_token')
        self.name = account_info.get('name')
        self.deviceId = account_info.get('deviceId')

        assert self.city_ver
        assert self.city_id
        assert self.ts_token
        assert self.name
        assert self.deviceId

        return True

    def save_account_config(self):
        assert self.city_ver
        assert self.city_id
        assert self.ts_token
        assert self.name
        assert self.deviceId

        path = self.account_path / "account_info.json"
        account_info = json.dumps({
            'city_ver': self.city_ver,
            'city_id': self.city_id,
            'ts_token': self.ts_token,
            'name' : self.name,
            'deviceId': self.deviceId,
        })
        path.write_bytes(account_info.encode('utf-8'))


    def _download_manifest(self, download_path: Path, data_path: Path):
        """
            download manifest.xml to `download_path`
            and also download files and extract zip files to `data_path` in its contents.

        Parameters
        ----------
        download_path
            download path from internet
        data_path
            decode or uncompress path from download file

        Returns
        -------

        """
        download_path.mkdir(mode=0o755, parents=True, exist_ok=True)
        filename = "manifest.xml"

        url = self.ts_request.get_url_township(filename)
        manifest_filename = download_path / filename

        if self.ts_request.request_get_and_download(url=url, download_file=manifest_filename):
            self._download_manifest_contents(manifest_filename, download_path, data_path)

        return True

    def _download_manifest_contents(self, manifest_filename, download_path, extract_path):
        tree = ElementTree.parse(manifest_filename)

        manifest = tree.getroot()
        assert manifest.tag == 'manifest', 'root node of {} tag is not manifest'.format(manifest_filename)

        for file in manifest.findall('file'):
            name = file.attrib.get('name', '')
            time = file.attrib.get('name', '')
            checksum = file.attrib.get('name', '')
            size = file.attrib.get('name', '')
            tag = file.attrib.get('tag', '')

            download_file = download_path / tag / name
            extract_to = extract_path

            url = self.ts_request.get_url_township(name)

            if self.ts_request.request_get_and_download(url=url, download_file=download_file):

                if '.zip' in name:
                    compressed_file = zipfile.ZipFile(download_file)
                    compressed_file.extractall(extract_to)
                else:
                    copy_to = extract_path / tag / name
                    copy_to.parent.mkdir(mode=0o755, parents=True, exist_ok=True)

                    try:
                        ts_decode_file(download_file, copy_to)
                    except:
                        copy_to.write_bytes(
                            download_file.read_bytes()
                        )

    def update_manifest(self):
        download_path = self.contents_path / "download"
        data_path = self.contents_path / "data"

        self._download_manifest(download_path, data_path)

    def update_base_content(self, base_path: Path, data_path: Path):
        base_path.mkdir(0o755, parents=True, exist_ok=True)
        data_path.mkdir(0o755, parents=True, exist_ok=True)
        for file in base_path.iterdir():
            if not file.is_file():
                continue
            target_file = data_path / file.name
            if target_file.exists():
                continue
            ts_decode_file(file, target_file)

    def _download_online_setting_country(self, download_path: Path, data_path: Path):
        """
            download manifest.xml to `download_path`
            and also download files and extract zip files to `data_path` in its contents.

        Parameters
        ----------
        download_path
            download path from internet
        data_path
            decode or uncompress path from download file

        Returns
        -------

        """
        download_path.mkdir(mode=0o755, parents=True, exist_ok=True)
        filename = "KR.json"

        url = self.ts_request.get_url_online_setting_country()
        country_filename = download_path / filename

        self.ts_request.request_get_and_download(url=url, download_file=country_filename)

        extract_to = data_path / filename
        if country_filename.exists():
            try:
                ts_decode_file(country_filename, extract_to)
            except:
                log.exception(name=__name__, func='online-setting: country', msg='Failed to decode file')
                extract_to.write_bytes(
                    country_filename.read_bytes()
                )

        return True

    def _download_online_setting_version(self, download_path: Path, data_path: Path):
        """
            download manifest.xml to `download_path`
            and also download files and extract zip files to `data_path` in its contents.

        Parameters
        ----------
        download_path
            download path from internet
        data_path
            decode or uncompress path from download file

        Returns
        -------

        """
        download_path.mkdir(mode=0o755, parents=True, exist_ok=True)
        filename = "settings.json"

        url = self.ts_request.get_url_online_setting_version()
        version_filename = download_path / filename

        self.ts_request.request_get_and_download(url=url, download_file=version_filename)

        extract_to = data_path / filename
        if version_filename.exists():
            try:
                ts_decode_file(version_filename, extract_to)
            except:
                log.exception(name=__name__, func='online-setting: settings', msg='Failed to decode file')
                extract_to.write_bytes(
                    version_filename.read_bytes()
                )

        return True

    def update_online_setting_country(self):
        download_path = self.contents_path / "download"
        data_path = self.contents_path / "data"

        self._download_online_setting_country(download_path, data_path)

    def update_online_setting_version(self):
        download_path = self.contents_path / "download"
        data_path = self.contents_path / "data"

        self._download_online_setting_version(download_path, data_path)

    def fetch_game_info(self) -> bool:
        """
            request FetchCity
            and save response.
            and parsing.
        Returns
        -------

        """

        if not self.fetch_city_header.exists() or not self.fetch_city_body.exists():
            filename = 'FetchCity'
            param = {
                'cityId': ''
            }
            dictbody = {
                'cityId': '',
                'cityVer': self.city_ver,
                'fetchCityId': self.city_id,
                'important': True,
            }
            headers = {
                'ts-bp': 'i',
                'ts-bver': settings.TS_APP_BVER,
                'ts-fver': settings.TS_APP_FVER,
                'ts-gpid': 'new',
                'ts-id': ''
            }
            bytebody = bytearray([])

            self._generate_body_and_update_ts_id(request_body=dictbody, ref_body=bytebody, ref_header=headers)

            url = self.ts_request.get_api_township(filename=filename, params=param)

            self.ts_request.request_post_and_download(
                url=url,
                body=bytebody,
                headers=headers,
                header_file=self.fetch_city_header,
                body_file=self.fetch_city_body,
            )

        return self.fetch_city_header.exists() and self.fetch_city_body.exists()

    def parse_fetch_city(self) -> bool:
        """
            parse (decode) fetch city info
        Returns
        -------

        """
        if not self.fetch_city_header.exists() or not self.fetch_city_body.exists():
            return False

        resp_headers = json.loads(self.fetch_city_header.read_bytes())
        ts_id = resp_headers.get('ts-id')
        resp_body = self.fetch_city_body.read_bytes()

        decoded_body = ts_aes_decode_with_tsid(body=resp_body, ts_id=ts_id)
        uncompress_body = ts_uncompress(decoded_body)
        self.fetch_city_decode.write_bytes(uncompress_body)

        json_body = json.loads(uncompress_body, strict=False)
        data = json_body.get('result', {}).get('data', None)
        if data:
            data = bytearray(base64.b64decode(data))
            data = ts_uncompress(
                ts_decode_bytearray(data, len(data))
            )
            self.fetch_city_data_decode.write_bytes(data)

        city_ver = int(json_body.get('result', {}).get('ver'))
        if city_ver > self.city_ver:
            self.city_ver = city_ver

        return True
    #
    # def generate_xml(self, elementTree, depth, outputs):
    #     attrs = []
    #     tab= "\t" * depth if depth > 0 else ''
    #     if elementTree.tag == "ABTests":
    #         pass
    #     if elementTree.attrib:
    #         for att in elementTree.attrib:
    #             if '"' in elementTree.attrib[att] or "'" in elementTree.attrib[att]:
    #                 pass
    #
    #             if '"' in elementTree.attrib[att]:
    #                 attrs.append(
    #                     "{}='{}'".format(att, elementTree.attrib[att].replace("'", "&apos;"))
    #                 )
    #             else:
    #                 attrs.append('{}="{}"'.format(att, elementTree.attrib[att]))
    #
    #     if len(elementTree) > 0:
    #         if attrs:
    #             outputs.append("{}<{} {}>".format(tab, elementTree.tag, ' '.join(attrs)))
    #         else:
    #             outputs.append("{}<{}>".format(tab, elementTree.tag))
    #
    #         for node in elementTree:
    #
    #             self.generate_xml(node, depth+1, outputs)
    #
    #         outputs.append("{}</{}>".format(tab, elementTree.tag))
    #     else:
    #         if attrs:
    #             outputs.append("{}<{} {}/>".format(tab, elementTree.tag, ' '.join(attrs)))
    #         else:
    #             outputs.append("{}<{}/>".format(tab, elementTree.tag))
    #
    # def load_game_info(self) -> bool:
    #     def add_val(root:ElementTree.Element, key, val):
    #         node = root.find(key)
    #         if node and 'v' in node.attrib:
    #             v = int(node.attrib['v'])
    #             node.attrib['v'] = str(v+val)
    #
    #     ts = int(datetime_to_timestamp(self.now))
    #
    #     json_body = json.loads(self.fetch_city_decode.read_bytes(), strict=False)
    #     prev_result = json_body.get('result', {})
    #     if 'data' in prev_result:
    #         del prev_result['data']
    #
    #     et = ElementTree.parse(self.fetch_city_data_decode)
    #     root = et.getroot()
    #     # add_val(root, './Global/Var[@name="wheatCounter"]', 1)
    #     # add_val(root, './Global/Var[@name="EarnedCoins"]', 1)
    #     # add_val(root, './Global/Var[@name="money"]', 1)
    #     root.find('./Global/Var[@name="saveGlobalTime"]').attrib['v'] = str(ts)
    #
    #     output = []
    #     self.generate_xml(root, 0, output)
    #     out_data = '\n'.join(output)
    #     out_data = out_data.replace(str(prev_result['ver']), str(ts))
    #     self.save_city_data.write_bytes(out_data.encode('utf-8'))
    #
    #     encode_data = _encode_x54(bytearray(self.save_city_data.read_bytes()))
    #     compress_data = ts_compress(encode_data)
    #     base64_data = base64.b64encode(compress_data).decode('utf-8')
    #
    #     json_data = {
    #             "bp": prev_result.get('bp', "\u0261"),
    #             "cash": int(root.find('./Global/Var[@name="moneyCash"]').attrib['v']),
    #             "ch": False,
    #             "ch_mark": "B,MV",
    #             "ch_reas": "",
    #             "cityId": self.city_id,
    #             "coins": int(root.find('./Global/Var[@name="money"]').attrib['v']),
    #             "data": base64_data,
    #             "deviceId": "da7682311424c714",
    #             "flw": prev_result.get('flw', 14),
    #             "gameId": root.find('./Global/Var[@name="gameId"]').attrib['v'],
    #             "gpId": root.find('./Global/Var[@name="PrevGCID"]').attrib['v'],
    #             "gpName": "DapperBeetle4729",
    #             "gsd": float(root.find('./Global/Var[@name="gameStartDate"]').attrib['v']),
    #             "help": "",
    #             "jb": True,
    #             "lang": prev_result.get('lang', 'en'),
    #             "lvl": prev_result.get('lvl', 'en'),
    #             "name": prev_result.get('name', 'DapperBeetle472'),
    #             "pf":  prev_result.get('pf', 14),
    #             "pic": root.find('./Global/Var[@name="MyPicture"]').attrib['v'],
    #             "prev": prev_result.get('ver', self.city_ver),
    #             "tz": 33400,
    #             "ver": ts,
    #             "xp": int(root.find('./Global/Var[@name="experience"]').attrib['v']),
    #             "zooac": 0
    #     }
    #
    #     filename = 'SaveCity'
    #     param = {
    #         'cityId': self.city_id
    #     }
    #
    #     headers = {
    #         'ts-bp': 'i',
    #         'ts-bver': settings.TS_APP_BVER,
    #         'ts-fver': settings.TS_APP_FVER,
    #         'ts-gpid': 'new',
    #         'ts-id': '',
    #         'ts-token': self.ts_token,
    #     }
    #     bytebody = bytearray([])
    #
    #     self._generate_body_and_update_ts_id(request_body=json_data, ref_body=bytebody, ref_header=headers)
    #     url = self.ts_request.get_api_township(filename=filename, params=param)
    #
    #     self.ts_request.request_post_and_download(
    #         url=url,
    #         body=bytebody,
    #         headers=headers,
    #         header_file=self.save_city_resp_header,
    #         body_file=self.save_city_resp_body,
    #     )
    #
    #     return True


class TsHelper(object):

    @classmethod
    def _generate_body_and_update_ts_id(cls, request_body: dict[str:Any], ref_body: bytearray, ref_header: dict[str:str]):

        json_body = json.dumps(request_body,  separators=(',', ':'))

        compress_body = ts_compress(json_body)

        out_dest = bytearray([0] * 16)
        iv = bytearray([random.randint(0, 255) for _ in range(12)])

        ts_aes_encode(
            key=settings.TS_AES_KEY,
            iv=iv,
            in_body=compress_body,
            out_buff=ref_body,
            out_dest=out_dest
        )

        ref_header.update({
            'ts-id': '002{}{}'.format(iv.hex(), out_dest.hex())
        })

        return True

    @classmethod
    def fetch_city(cls, city_ver: int, city_id: str, header_filename: Path, body_filename: Path):
        """
            Request 'FetchCity' and save response header and body
        """

        if header_filename.exists() and body_filename.exists():
            return True

        filename = 'FetchCity'
        param = {
            'cityId': ''
        }

        dictbody = {
            'cityId': '',
            'cityVer': city_ver,
            'fetchCityId': city_id,
            'important': True,
        }

        headers = {
            'ts-bp': 'i',
            'ts-bver': settings.TS_APP_BVER,
            'ts-fver': settings.TS_APP_FVER,
            'ts-gpid': 'new',
            'ts-id': ''
        }
        bytebody = bytearray([])

        cls._generate_body_and_update_ts_id(request_body=dictbody, ref_body=bytebody, ref_header=headers)

        url = TsRequest.get_api_township(filename=filename, params=param)

        TsRequest.request_post_and_download(
            url=url,
            body=bytebody,
            headers=headers,
            header_file=header_filename,
            body_file=body_filename,
        )

        return header_filename.exists() and body_filename.exists()

    @classmethod
    def parse_fetch_city(cls, ts_id: str, body_filename: Path,  decode_json_filename: Path, decode_xml_filename: Path):
        if not body_filename.exists():
            return False

        resp_body = body_filename.read_bytes()

        decoded_body = ts_aes_decode_with_tsid(body=resp_body, ts_id=ts_id)
        uncompress_body = ts_uncompress(decoded_body)
        decode_json_filename.write_bytes(uncompress_body)

        json_body = json.loads(uncompress_body, strict=False)
        data = json_body.get('result', {}).get('data', None)
        if data:
            data = bytearray(base64.b64decode(data))

            data = ts_uncompress(
                ts_decode_bytearray(data, len(data))
            )
            decode_xml_filename.write_bytes(data)

        return True

    @classmethod
    def CheckCity(cls, cityId, token, header_filename, body_filename, decode_filename):
        filename = 'CheckCity'
        param = {
            'cityId': cityId
        }

        dictbody = {
            'cityId': cityId,
            'tz': -21600,
        }

        headers = {
            'ts-bp': 'i',
            'ts-bver': settings.TS_APP_BVER,
            'ts-fver': settings.TS_APP_FVER,
            'ts-gpid': 'new',
            'ts-id': '',
            'ts-token': token
        }
        bytebody = bytearray([])

        cls._generate_body_and_update_ts_id(request_body=dictbody, ref_body=bytebody, ref_header=headers)

        url = TsRequest.get_api_township(filename=filename, params=param)

        TsRequest.request_post_and_download(
            url=url,
            body=bytebody,
            headers=headers,
            header_file=header_filename,
            body_file=body_filename,
        )
        resp_headers = json.loads(header_filename.read_bytes())
        ts_id = resp_headers.get('ts-id')
        resp_body = body_filename.read_bytes()

        body = ts_aes_decode_with_tsid(resp_body, ts_id)
        ts_decode_file(body_filename, decode_filename)


    @classmethod
    def save_city(cls, json_data: Dict, city_id: str, ts_token: str, header_filename: Path, body_filename: Path):
        filename = 'SaveCity'
        param = {
            'cityId': city_id
        }

        headers = {
            'ts-bp': 'i',
            'ts-bver': settings.TS_APP_BVER,
            'ts-fver': settings.TS_APP_FVER,
            'ts-gpid': 'new',
            'ts-id': '',
            'ts-token': ts_token,
        }

        bytebody = bytearray([])

        cls._generate_body_and_update_ts_id(request_body=json_data, ref_body=bytebody, ref_header=headers)

        url = TsRequest.get_api_township(filename=filename, params=param)

        TsRequest.request_post_and_download(
            url=url,
            body=bytebody,
            headers=headers,
            header_file=header_filename,
            body_file=body_filename,
        )

        return header_filename.exists() and body_filename.exists()
