import json
import time
from pathlib import Path
from typing import List, Union

import requests
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from core.utils import Logger

log = Logger('default')


class TsRequest(object):

    @classmethod
    def get_url_online_setting_country(cls):
        return f'https://{settings.URL_CDN_PLAYRIX}/online-settings/Township/production/{settings.TS_APP_OS}/country/{settings.TS_APP_COUNTRY}.json'

    @classmethod
    def get_url_online_setting_version(cls):
        return f'https://{settings.URL_CDN_PLAYRIX}/online-settings/Township/production/{settings.TS_APP_OS}/{settings.TS_APP_VERSION}/settings.json'

    @classmethod
    def get_url_township(cls, filename):
        return f'https://{settings.URL_CDN_TOWNSHIP}/{settings.TS_APP_DOWNLOAD_TYPE}/{settings.TS_APP_VERSION}/{filename}'

    @classmethod
    def get_api_township(cls, filename, params={}):
        if params:
            p = '&'.join(['{}={}'.format(k, params.get(k,'')) for k in params])
        else:
            p = ''

        if p:
            return f'https://{settings.URL_API_TOWNSHIP}/api/1/{filename}?{p}'
        else:
            return f'https://{settings.URL_API_TOWNSHIP}/api/1/{filename}'

    @classmethod
    def _get(cls, url, headers={}):
        with requests.Session() as s:
            req = requests.Request(method='GET', url=url, headers=headers)
            p = req.prepare()

            r = s.send(p)

            r.raise_for_status()

            return r

    @classmethod
    def _post(cls, url, body, headers={}):
        with requests.Session() as s:
            req = requests.Request(method='POST', url=url, headers=headers, data=body)
            p = req.prepare()

            r = s.send(p)

            r.raise_for_status()

            return r

    @classmethod
    def request_get_and_download(cls, url: str, download_file: Path, overwrite=False):
        headers = {
            'Content-Type': 'text/plain'
        }
        if download_file.exists() and not overwrite:
            ts = download_file.lstat().st_ctime  # fixme: depend on os
            created = datetime.fromtimestamp(ts, tz=timezone.get_current_timezone())

            headers.update({
                'if-modified-since': created.strftime('%a, %d %b %Y %X %Z')
            })

        download_file.parent.mkdir(mode=0o755, parents=True, exist_ok=True)

        resp = cls._get(url=url, headers=headers)

        if resp.status_code == 304:
            # not modified.
            return False
        elif resp.status_code == 200:
            download_file.write_bytes(resp.content)
            return True

        return False

    @classmethod
    def request_post_and_download(cls, url: str, body: Union[None, bytes, bytearray], headers: dict, header_file: Path, body_file: Path):
        headers.update({
            'Content-Type': 'application/octet-stream'
        })

        required_header_fields = [
            'ts-bp', 'ts-bver', 'ts-fver', 'ts-gpid', 'ts-id'
        ]

        assert headers
        for key in required_header_fields:
            assert key in headers
            assert headers[key]

        resp = cls._post(
            url=url,
            body=body,
            headers=headers
        )

        resp.raise_for_status()

        if resp:
            header_file.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
            body_file.parent.mkdir(mode=0o755, parents=True, exist_ok=True)

            if resp.headers:
                headers = {}
                for k in resp.headers:
                    headers.update({k: resp.headers.get(k)})

                header_file.write_bytes(json.dumps(headers).encode('utf-8'))
            if resp.content:
                body_file.write_bytes(resp.content)

            return True

        return False
