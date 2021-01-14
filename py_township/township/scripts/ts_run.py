import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytz
from django.conf import settings
from django.utils import timezone

from app_root.contents.models import TownshipVersion
from app_root.gameinfos.models import Account, GameInfo
from app_root.gameinfos.utils import update_city, parse_township_data, XmlParser, update_township_data, \
    save_township_data
from core.utils import Logger
from modules.ts_helper import TsHelper

log = Logger('default')


def run():
    version = TownshipVersion.objects.order_by('-version').first()

    for account in Account.objects.all():
        now = timezone.now().astimezone(pytz.timezone('Asia/Seoul'))
        yyyymmdd = now.strftime('%Y%m%d')
        hhmmss = now.strftime('%H%M%S')

        game_info = None # GameInfo.objects.filter(account=account, version=version, id=5).order_by('pk').last()
        account_path = settings.WORK_DIR / 'accounts' / settings.TS_APP_VERSION / account.alias / yyyymmdd / hhmmss
        TsHelper.CheckCity(
            cityId=account.city_id,
            header_filename=account_path / "check_city_header.log",
            body_filename=account_path / "check_city_body.log",
            decode_filename=account_path / "check_city_decode_body.log",
            token=account.ts_token,
        )
        continue

        if game_info is None:
            game_info = update_city(
                now=now,
                work_path=account_path,
                version=version,
                account=account
            )

        parser = XmlParser()
        parser.load_game_info(path=game_info.decode_data_path)
        time.sleep(1)

        parse_township_data(parser=parser, gameinfo=game_info)

        req_data = update_township_data(parser=parser, gameinfo=game_info)

        resp = None

        if req_data:
            resp = save_township_data(
                now=now,
                req_data=req_data,
                city_id=account.city_id,
                ts_token=account.ts_token,
                work_path=account_path
            )

        if isinstance(resp, dict):
            if 'ver' in resp:
                account.city_ver = resp['ver']
            if 'ts-token' in resp:
                account.ts_token = resp['ts-token']

            account.save()

