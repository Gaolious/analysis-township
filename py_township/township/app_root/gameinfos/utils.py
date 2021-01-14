import base64
import json
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
from xml.etree import ElementTree

import pytz
from django.conf import settings
from django.utils import timezone

from app_root.contents.models import TownshipVersion, Product, Building
from app_root.gameinfos.models import Account, GameInfo, BarnItem, Factory, FactoryItem, GlobalInfo
from app_root.gameinfos.ts_parsers.xml_nodes import GlobalNode, BuildingsNode, EtcNode, DevicesNode, TrainNode
from modules.ts_aes import ts_aes_decode_with_tsid
from modules.ts_file import _encode_0x79
from modules.ts_gzip import ts_compress, ts_uncompress
from modules.ts_helper import TsHelper
from core.utils import Logger
from modules.ts_utils import u32

log = Logger('default')

# calculate_hashes
def get_ghash(moneyCash: int) -> int:
    """
    moneyCash 의 hash 값. ( root > Global > moneyCash )
    Parameters
    ----------
    moneyCash

    Returns
    -------

    """
    h = 0x5BD1E995
    ha1 = u32(h * moneyCash)
    v1 = u32(h * (ha1 ^ (ha1 >> 24))) ^ 0x81504308
    v13 = u32(h * (v1 ^ (v1 >> 13)))
    v2 = v13 ^ (v13 >> 15)

    return -(0xffffffff + 1 - v2)


def get_sexpx(experience: int) -> int:
    return experience ^ 0x1E5D6A06


def get_whudup(WareHouseCashUpgrade: int) -> int:
    return WareHouseCashUpgrade ^ 0x1EADABCC


class XmlParser(object):
    mapping = {}

    def __init__(self):
        self.mapping = {
            'Global': GlobalNode(),
            'Buildings': BuildingsNode(),
            'Devices': DevicesNode(),
            'Trains': TrainNode(),
        }

    def get_train_node(self):
        return self.mapping['Trains']

    def get_global_node(self):
        return self.mapping['Global']

    def load_game_info(self, path: str):

        et = ElementTree.parse(path)
        root = et.getroot()

        for node in root:
            if node.tag not in self.mapping:
                self.mapping.update({node.tag: EtcNode()})

            obj = self.mapping.get(node.tag, None)

            if obj:
                obj.parse(node=node)

    def get_xml_string(self):
        ret = ["<root>"]
        for k in self.mapping:
            ret += self.mapping[k].get_xml_string(depth=1)
        ret += ["</root>"]

        return '\n'.join(ret)

    """
        sub_11ECDBE((int)&v16, "gem1", "sgc1x");
        sub_11ECDBE((int)&v18, "gem2", "sgc2x");
        sub_11ECDBE((int)&v19, "gem3", "sgc3x");
        sub_11ECDBE((int)&v20, "gem4", "sgc4x");
        sub_11ECE20((int)&v21, "GoldBullionCounter", "sgbcx");
        sub_11ECE82((int)&v22, "SilverBullionCounter", "ssbcx");
        sub_11ECE82((int)&v23, "BronzeBullionCounter", "sbbcx");
        sub_11ECEE4((int)&v24, "PlatinumBullionCounter", "spbcx");
        sub_11ECF46((int)&v25, "m1", "sm1x");
        sub_11ECF46((int)&v26, "m2", "sm2x");
        sub_11ECF46((int)&v27, "m3", "sm3x");
        sub_11ECFA8((int)&v28, "zoo_level", "szlx");
        sub_11ED00A((int)&v29, "experience", "sexpx");    
        scsx - 쿠폰
    """

    def get_experience(self):
        global_node = self.get_global_node()
        return int(global_node.child_dict['experience'].attrs['v'])

    def set_experience(self, new_exp: int):
        global_node = self.get_global_node()

        global_node.child_dict['experience'].attrs['v'] = str(new_exp)
        global_node.child_dict['sexpx'].attrs['v'] = str(get_sexpx(new_exp))


def update_city(now: datetime, work_path: Path, version: TownshipVersion, account: Account) -> Optional[GameInfo]:
    fetch_city_path = work_path / "fetch_city"
    fetch_city_resp_header_filename = fetch_city_path / settings.FETCH_CITY_RESP_HEADER_FILENAME
    fetch_city_resp_body_filename = fetch_city_path / settings.FETCH_CITY_RESP_BODY_FILENAME

    decode_city_json = fetch_city_path / settings.FETCH_CITY_DECODE_JSON_FILENAME
    decode_city_xml = fetch_city_path / settings.FETCH_CITY_DECODE_XML_FILENAME

    ret = TsHelper.fetch_city(
        city_ver=account.city_ver,
        city_id=account.city_id,
        header_filename=fetch_city_resp_header_filename,
        body_filename=fetch_city_resp_body_filename,
    )

    if not ret:
        return None

    resp_headers = json.loads(fetch_city_resp_header_filename.read_bytes())
    ts_id = resp_headers.get('ts-id')

    ret = TsHelper.parse_fetch_city(
        ts_id=ts_id,
        body_filename=fetch_city_resp_body_filename,
        decode_json_filename=decode_city_json,
        decode_xml_filename=decode_city_xml
    )

    if not ret:
        return None

    data = json.loads(decode_city_json.read_bytes())
    result = data.get('result', {})

    return GameInfo.objects.create(
        account=account,
        version=version,
        fetch_city_header_path=fetch_city_resp_header_filename,
        fetch_city_body_path=fetch_city_resp_body_filename,
        decode_body_path=decode_city_json,
        decode_data_path=decode_city_xml,
        fetch_city_ts_id=ts_id,
        fver=result.get('fver'),
        ver=result.get('ver'),
        dkey=result.get('dkey'),
        updat=result.get('updAt'),
        likes=result.get('likes'),
        lvl=result.get('lvl'),
        cash=result.get('cash'),
        pic=result.get('pic'),
        name=result.get('name'),
        bp=result.get('bp'),
        lang=result.get('lang'),
        flw=result.get('flw'),
        cityId=result.get('cityId'),
        pf=result.get('pf'),
        jb=result.get('jb'),
        xp=result.get('xp'),
        coins=result.get('coins'),
        gameId=result.get('gameId'),
        bver=result.get('bver'),
        tz=result.get('tz'),
        ernies_likes=result.get('ernies_likes'),
    )


def update_global_info(parser: XmlParser, gameinfo: GameInfo):

    globalNode: GlobalNode = parser.mapping.get('Global')

    info = GlobalInfo.objects.filter(gameinfo=gameinfo).first()
    if info:
        return info

    GlobalInfo.objects.create(
        gameinfo=gameinfo,
        orderSeq=globalNode.get_attr_value(key='orderSeq'),
        money=globalNode.get_attr_value('money'),
        moneyCash=globalNode.get_attr_value('moneyCash'),
        maxResidents=globalNode.get_attr_value('maxResidents'),
        lastVisitDay=globalNode.get_attr_value('lastVisitDay'),
        lastVisitDayEBR=globalNode.get_attr_value('lastVisitDayEBR'),
        lastVisitSaleDay=globalNode.get_attr_value('lastVisitSaleDay'),
        levelup=globalNode.get_attr_value(key='levelup'),
        var_hex=globalNode.get_attr_value(key='hex'),
        var_hex2=globalNode.get_attr_value(key='hex2'),
        gameStartDate=globalNode.get_attr_value(key='gameStartDate'),
        gameId=globalNode.get_attr_value(key='gameId'),
        factoryTime=globalNode.get_attr_value(key='factoryTime'),
        earnedCash=globalNode.get_attr_value(key='earnedCash'),
        experience=globalNode.get_attr_value(key='experience'),
        dayInGame=globalNode.get_attr_value(key='dayInGame'),
        changeVarTimestamp=globalNode.get_attr_value(key='changeVarTimestamp'),
        timeInGame=globalNode.get_attr_value(key='timeInGame'),
        townName=globalNode.get_attr_value(key='townName'),
        saveGlobalTime=globalNode.get_attr_value(key='saveGlobalTime'),
        GHash=globalNode.get_attr_value(key='GHash'),
        FVer=globalNode.get_attr_value(key='FVer'),
        EarnedCoins=globalNode.get_attr_value(key='EarnedCoins'),
        ExpandLevel=globalNode.get_attr_value(key='ExpandLevel'),
        CTTime=globalNode.get_attr_value(key='CTTime'),
        AirScore2=globalNode.get_attr_value(key='AirScore2'),
        AirScore1=globalNode.get_attr_value(key='AirScore1'),
        AirVersion=globalNode.get_attr_value(key='AirVersion'),
        WHUdup=globalNode.get_attr_value(key='WHUdup'),
        VCheckTime=globalNode.get_attr_value(key='VCheckTime'),
        SCOrders=globalNode.get_attr_value(key='SCOrders'),
        SCTime=globalNode.get_attr_value(key='SCTime'),
        SBCTime=globalNode.get_attr_value(key='SBCTime'),
        PrevGCID=globalNode.get_attr_value(key='PrevGCID'),
    )


def update_barn_info(parser: XmlParser, gameinfo: GameInfo):
    if BarnItem.objects.filter(gameinfo=gameinfo).exists():
        return

    BarnItem.objects.filter(gameinfo=gameinfo).delete()

    globalNode: GlobalNode = parser.mapping.get('Global')

    bulk_list = []

    for product in Product.objects.all():
        if product.level_need > gameinfo.lvl:
            continue

        cnt = globalNode.get_attr_value(key=product.product_id)
        if cnt is None:
            continue
        obj = BarnItem(
            gameinfo=gameinfo,
            product=product,
            amount=cnt,
        )

        bulk_list.append(obj)

    if bulk_list:
        BarnItem.objects.bulk_create(
            bulk_list
        )


def update_factory_info(parser: XmlParser, gameinfo: GameInfo):

    building_node: BuildingsNode = parser.mapping.get('Buildings')

    # buildings base on contents
    for building in Building.objects.filter(building_type=Building.TYPE_BUILDING_FACTORY).all():

        # buildings base on FetchCity
        for factory_building in building_node.get_buildings_by_id(building_id=building.building_id):
            data = factory_building.attrs.get('data', {})
            order_count = data.get('ordersCount')
            if order_count is None:
                continue

            factory = Factory.objects.filter(gameinfo=gameinfo, bid=data.get('bid')).first()
            if not factory:
                factory = Factory.objects.create(
                    gameinfo=gameinfo,
                    building=building,
                    pos_i=data.get('i'),
                    pos_j=data.get('j'),
                    bid=data.get('bid'),
                    check_time=data.get('time'),
                    state=data.get('state'),
                    slot_count=data.get('slotsCount'),
                )

            factory_item_list = []
            for i in range(int(order_count)):
                order_time_key = 'orderTime{}'.format(i)
                order_max_time_key = 'orderMaxTime{}'.format(i)
                product_id_key = 'productId{}'.format(i)
                amount_key = 'amount{}'.format(i)

                product = Product.objects.filter(
                    product_id=data.get(product_id_key)
                ).first()

                if not product:
                    product = Product.objects.filter(
                        product_name=data.get(product_id_key)
                    ).first()

                assert product

                if FactoryItem.objects.filter(factory=factory, product=product, idx=i).exists():
                    continue
                factory_item_list.append(
                    FactoryItem(
                        factory=factory,
                        product=product,
                        amount=data.get(amount_key, 1),
                        idx=i,
                        order_time=data.get(order_time_key, 0),
                        order_max_time=data.get(order_max_time_key, 0)
                    )
                )
            if factory_item_list:
                FactoryItem.objects.bulk_create(factory_item_list)


def base62_encode(val: int) -> str:
    M = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    lenM = len(M)

    divisor = lenM
    ret = []
    while val > 0:
        ret.append(M[val % lenM])
        val //= divisor

    return ''.join(reversed(ret))

def base62_decode(val: str) -> int:
    M = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    lenM = len(M)
    divisor = lenM

    ret = 0
    for c in val:
        ret = ret * divisor + M.index(c)
    return ret


def update_train_info(parser: XmlParser, gameinfo: GameInfo):
    train_node = parser.get_train_node()

    for train in train_node.childs:

        attr = train.attrs.get('v', {})

        i = 1
        while True:
            order_id_key = 'orderId_{}'.format(i)
            if order_id_key not in attr:
                break

            a, b = attr[order_id_key].split('-')

            i += 1

        pass
    """
    도착 직후
<Trains>
<train v="{"guid":"1kuj8j-Bbu","startTime":1609421307,
    "matId_1":"Glass","matId_2":"Brick","matId_3":"Plita","matId_4":"","matId_5":"","materialsGenerated":1,
    "trainTimeInProgress":600.0,"cityId":3,"sended":1,
    "productId_1":"corn","productCount_1":1,"productDone_1":1,"orderId_1":"1kuxpA-SZ3",
    "productId_2":"corn","productCount_2":1,"productDone_2":1,"orderId_2":"1kuxpA-fZ3",
    "productId_3":"bread","productCount_3":1,"productDone_3":1,"orderId_3":"1kuxpA-sZ3",
    "productId_4":"","productCount_4":0,"orderId_4":"1kuxpL-5a3",
    "productId_5":"","productCount_5":0,"orderId_5":"1kuxpL-Ia3",
    "wasVisible":1}"/>

</Trains>
    아이템 1개 싣고
<Trains>
    <train v="{"guid":"1kuj8j-Bbu","startTime":1609425548,"matId_1":"","matId_2":"","matId_3":"","matId_4":"","matId_5":"",
    "trainTimeInProgress":600.0,"cityId":3,
    "productId_1":"carrot","productCount_1":1,"orderId_1":"1kuz6a-teM",
    "productId_2":"carrot","productCount_2":1,"orderId_2":"1kuz6a-6fM",
    "productId_3":"milk","productCount_3":1,"productDone_3":1,"orderId_3":"1kuz6a-JfM",
    "productId_4":"","productCount_4":0,"orderId_4":"1kuz6v-WfM","productId_5":"","productCount_5":0,"orderId_5":"1kuz6v-jfM"}"/>
</Trains>

기차 보낸 후
    <train v="{"guid":"1kuj8j-Bbu","startTime":1609427463,"matId_1":"","matId_2":"","matId_3":"","matId_4":"","matId_5":"",
    "trainTimeInProgress":600.0,"cityId":11,
    "sended":1,"productId_1":"carrot","productCount_1":1,"productDone_1":1,"orderId_1":"1kuz6a-teM",
    "productId_2":"carrot","productCount_2":1,"productDone_2":1,"orderId_2":"1kuz6a-6fM",
    "productId_3":"milk","productCount_3":1,"productDone_3":1,"orderId_3":"1kuz6a-JfM",
    "productId_4":"","productCount_4":0,"orderId_4":"1kuz6v-WfM",
    "productId_5":"","productCount_5":0,"orderId_5":"1kuz6v-jfM"}"/>
    Parameters
    ----------
    parser
    gameinfo

    Returns
    -------

    """
    pass

def parse_township_data(parser: XmlParser, gameinfo: GameInfo):

    update_global_info(parser=parser, gameinfo=gameinfo)

    update_barn_info(parser=parser, gameinfo=gameinfo)

    update_factory_info(parser=parser, gameinfo=gameinfo)

    update_train_info(parser=parser, gameinfo=gameinfo)

def _generate_encoded_data(parser: XmlParser):
    xml_string = parser.get_xml_string()
    xml_compress = ts_compress(xml_string)
    encode_xml = _encode_0x79(xml_compress)

    data = base64.b64encode(encode_xml)
    return data.decode('utf-8')


def _generate_request_dict_data(gameinfo: GameInfo, ts):
    global_info: GlobalInfo = gameinfo.global_info.first()

    dict_data = {
        "bp": "\u0261",
        "cash": global_info.moneyCash,
        "ch": False,
        "ch_mark": "B",
        "ch_reas": "",
        "cityId": gameinfo.cityId,
        "coins": global_info.money,
        "data": '',
        "deviceId": "da7682311424c714",
        "flw": gameinfo.flw,
        "gameId": gameinfo.gameId,
        "gpId": global_info.PrevGCID,
        "gpName": "DapperBeetle4729",
        "gsd": float(global_info.gameStartDate),
        "help": "",
        "jb": gameinfo.jb,
        "lang": gameinfo.lang,
        "lvl": gameinfo.lvl,
        "name": "DapperBeetle472",
        "pf": gameinfo.pf,
        "pic": gameinfo.pic,
        "prev": gameinfo.ver,
        "tz": -20600,
        "ver": ts,
        "xp": gameinfo.xp,
        "zooac": 0
    }
    return dict_data


def modify_township_data(parser: XmlParser, gameinfo: GameInfo):
    pass


def add_experience(delta_exp: int, parser: XmlParser, gameinfo: GameInfo):
    xp = gameinfo.xp + delta_exp

    gameinfo.xp = xp
    parser.set_experience(xp)


def update_township_data(parser: XmlParser, gameinfo: GameInfo):

    now = timezone.now().astimezone(pytz.timezone('Asia/Seoul'))
    ts = int(time.mktime(now.timetuple()))

    log.debug(
        name=__name__, func='update_township_data',
        fetch_ts=gameinfo.ver,
        fetch_dt=datetime.fromtimestamp(gameinfo.ver, pytz.timezone('Asia/Seoul')).strftime('%Y%m%d_%H%M%S'),
        now_ts=ts,
        now_dt=now.strftime('%Y%m%d_%H%M%S'),
    )

    for key in parser.mapping:
        parser.mapping[key].update_timestamp(ts=ts)
    #
    # add_experience(delta_exp=1, parser=parser, gameinfo=gameinfo)

    data = _generate_encoded_data(parser)

    dict_data = _generate_request_dict_data(gameinfo=gameinfo, ts=ts)
    log.debug(
        name=__name__, func='update_township_data',
        dict_data=dict_data
    )

    dict_data.update({
        'data': data
    })

    return dict_data


def save_township_data(now:datetime, req_data: Dict, city_id: str, ts_token: str, work_path: Path):

    save_city_path = work_path / "save_city"

    header_filename = save_city_path / "resp_header.txt"
    body_filename = save_city_path / "resp_body.txt"

    decode_body_filename = save_city_path / "decode_resp_body.txt"

    ret = TsHelper.save_city(
        json_data=req_data,
        city_id=city_id,
        ts_token=ts_token,
        header_filename=header_filename,
        body_filename=body_filename
    )

    if not ret:
        return None

    body = body_filename.read_bytes()
    ts_id = json.loads(header_filename.read_bytes().decode('utf-8'))['ts-id']

    decoded_body = ts_aes_decode_with_tsid(body=body, ts_id=ts_id)
    uncompress_body = ts_uncompress(decoded_body)
    decode_body_filename.write_bytes(uncompress_body)

    resp_body = json.loads(uncompress_body.decode('utf-8'))

    return resp_body.get('result', {})

