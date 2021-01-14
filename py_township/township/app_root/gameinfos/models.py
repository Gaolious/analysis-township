import time
from datetime import datetime

import pytz
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from core.models.mixins import CreatedModelMixin


class Account(CreatedModelMixin):

    alias = models.CharField(_('alias'), max_length=64, null=False, blank=False)

    ts_token = models.CharField(_('ts_token'), max_length=64, null=False, blank=False)

    city_ver = models.BigIntegerField(_('city_ver'), null=False, blank=False)

    city_id = models.CharField(_('city id'), max_length=20, null=False, blank=False)

    name = models.CharField(_('name'), max_length=100, null=False, blank=False)

    device_id = models.CharField(_('device id'), max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = 'account'
        verbose_name_plural = 'accounts'
        ordering = ['-pk']

    def __str__(self):
        return self.alias


class GameInfo(CreatedModelMixin):
    account = models.ForeignKey(
        to='gameinfos.Account',
        on_delete=models.deletion.DO_NOTHING,
        related_name='gameinfos',
        db_constraint=False,
        blank=False,
        null=False,
    )

    version = models.ForeignKey(
        to='contents.TownshipVersion',
        on_delete=models.deletion.DO_NOTHING,
        related_name='gameinfos',
        db_constraint=False,
        blank=False,
        null=False,
    )

    fetch_city_header_path = models.CharField(_('fetch city header path'), max_length=2048, null=False, blank=False)
    fetch_city_body_path = models.CharField(_('fetch city body path'), max_length=2048, null=False, blank=False)

    decode_body_path = models.CharField(_('decode body path'), max_length=2048, null=False, blank=False)
    decode_data_path = models.CharField(_('decode data path'), max_length=2048, null=False, blank=False)

    fetch_city_ts_id = models.CharField(_('fetch city ts_id'), max_length=50, null=False, blank=False)

    bp = models.CharField(_('bp'), max_length=50, null=False, blank=False)
    cash = models.PositiveIntegerField(_('cash'), null=False, blank=False)
    ch = models.BooleanField(_('ch'), null=True, blank=False)
    cityId = models.CharField(_('city id'), max_length=50, null=False, blank=False)
    coins = models.PositiveIntegerField(_('coins'), null=False, blank=False)
    deviceId = models.CharField(_('deviceId'), max_length=100, null=False, blank=False)
    flw = models.PositiveIntegerField(_('flw'), null=True, blank=False)
    gameId = models.CharField(_('gameId'), max_length=50, null=True, blank=False)
    gpId = models.CharField(_('gpId'), max_length=50, null=True, blank=False)
    gpName = models.CharField(_('gpName'), max_length=50, null=True, blank=False)
    gsd = models.FloatField(_('gsd'), null=True, blank=False)
    help = models.CharField(_('help'), max_length=10240, null=True, blank=False)
    jb = models.BooleanField(_('pf'), null=True, blank=False)
    lang = models.CharField(_('lang'), max_length=50, null=True, blank=False)
    lvl = models.PositiveIntegerField(_('level'), null=True, blank=False)
    name = models.CharField(_('name'), max_length=50, null=True, blank=False)
    pf = models.BooleanField(_('pf'), null=True, blank=False)
    pic = models.CharField(_('pic'), max_length=50, null=True, blank=False)

    prev = models.BigIntegerField(_('ver'), null=True, blank=False)
    tz = models.IntegerField(_('tz'), null=True, blank=False)
    ver = models.BigIntegerField(_('ver'), null=True, blank=False)
    xp = models.PositiveIntegerField(_('xp'), null=True, blank=False)
    zooac = models.PositiveIntegerField(_('zooac'), null=True, blank=False)

    fver = models.PositiveIntegerField(_('fver'), null=True, blank=False)
    dkey = models.CharField(_('dkey'), max_length=20, null=True, blank=False)
    updat = models.BigIntegerField(_('updAt'), null=True, blank=False)
    likes = models.PositiveIntegerField(_('likes'), null=True, blank=False)
    bver = models.CharField(_('bver'), max_length=50, null=True, blank=False)
    ernies_likes = models.BigIntegerField(_('ernies likes'), null=True, blank=False)

    class Meta:
        verbose_name = 'gameinfo'
        verbose_name_plural = 'gameinfos'
        ordering = ['-pk']

    def get_request_dict(self):
        ret = {
            'bp': self.bp if self.bp is not None else '',
            'cash': self.cash if self.cash is not None else 0,
            'ch': self.ch if self.ch is not None else False,
            'cityId': self.cityId if self.cityId is not None else '',
            'coins': self.coins if self.coins is not None else 0,
            'deviceId': self.deviceId if self.deviceId is not None else '',
            'flw': self.flw if self.flw is not None else 0,
            'gameId': self.gameId if self.gameId is not None else '',
            'gpId': self.gpId if self.gpId is not None else '',
            'gpName': self.gpName if self.gpName is not None else '',
            'gsd': self.gsd if self.gsd is not None else 0.0,
            'help': self.help if self.help is not None else '',
            'jb': self.jb if self.jb is not None else False,
            'lang': self.lang if self.lang is not None else '',
            'lvl': self.lvl if self.lvl is not None else 0,
            'name': self.name if self.name is not None else '',
            'pf': self.pf if self.pf is not None else False,
            'pic': self.pic if self.pic is not None else '',
            'prev': self.prev if self.prev is not None else 0,
            'tz': self.tz if self.tz is not None else 0,
            'ver': self.ver if self.ver is not None else 0,
            'xp': self.xp if self.xp is not None else 0,
            'zooac': self.zooac if self.zooac is not None else 0,
        }

        return ret

class GlobalInfo(CreatedModelMixin):
    gameinfo = models.ForeignKey(
        to='gameinfos.GameInfo',
        on_delete=models.deletion.DO_NOTHING,
        related_name='global_info',
        db_constraint=False,
        blank=False,
        null=False,
    )
    orderSeq = models.PositiveIntegerField(_('orderSeq'), null=True, blank=False)
    money = models.PositiveIntegerField(_('money'), null=True, blank=False)
    moneyCash = models.PositiveIntegerField(_('moneyCash'), null=True, blank=False)
    maxResidents = models.PositiveIntegerField(_('maxResidents'), null=True, blank=False)
    lastVisitDay = models.PositiveIntegerField(_('lastVisitDay'), null=True, blank=False)
    lastVisitDayEBR = models.PositiveIntegerField(_('lastVisitDayEBR'), null=True, blank=False)
    lastVisitSaleDay = models.PositiveIntegerField(_('lastVisitSaleDay'), null=True, blank=False)
    levelup = models.PositiveIntegerField(_('levelup'), null=True, blank=False)
    var_hex = models.CharField(_('hex'), max_length=50, null=True, blank=False)
    var_hex2 = models.CharField(_('hex2'), max_length=50, null=True, blank=False)
    gameStartDate = models.BigIntegerField(_('gameStartDate'), null=True, blank=False)
    gameId = models.CharField(_('gameId'), max_length=50, null=True, blank=False)
    factoryTime = models.BigIntegerField(_('factoryTime'), null=True, blank=False)

    earnedCash = models.PositiveIntegerField(_('earnedCash'), null=True, blank=False)
    experience = models.BigIntegerField(_('experience'), null=True, blank=False)
    dayInGame = models.PositiveIntegerField(_('dayInGame'), null=True, blank=False)
    changeVarTimestamp = models.BigIntegerField(_('changeVarTimestamp'), null=True, blank=False)

    timeInGame = models.FloatField(_('timeInGame'), null=True, blank=False)
    townName = models.CharField(_('townName'), max_length=50, null=True, blank=False)
    saveGlobalTime = models.BigIntegerField(_('saveGlobalTime'), null=True, blank=False)
    GHash = models.BigIntegerField(_('GHash'), null=True, blank=False)

    FVer = models.PositiveIntegerField(_('FVer'), null=True, blank=False)
    EarnedCoins = models.PositiveIntegerField(_('EarnedCoins'), null=True, blank=False)
    ExpandLevel = models.PositiveIntegerField(_('ExpandLevel'), null=True, blank=False)
    CTTime = models.PositiveIntegerField(_('CTTime'), null=True, blank=False)

    AirScore2 = models.PositiveIntegerField(_('AirScore2'), null=True, blank=False)
    AirScore1 = models.PositiveIntegerField(_('AirScore1'), null=True, blank=False)
    AirVersion = models.PositiveIntegerField(_('AirVersion'), null=True, blank=False)
    WHUdup = models.PositiveIntegerField(_('WHUdup'), null=True, blank=False)
    VCheckTime = models.BigIntegerField(_('VCheckTime'), null=True, blank=False)
    SCOrders = models.BigIntegerField(_('SCOrders'), null=True, blank=False)
    SCTime = models.BigIntegerField(_('SCTime'), null=True, blank=False)
    SBCTime = models.BigIntegerField(_('SBCTime'), null=True, blank=False)
    PrevGCID = models.CharField(_('PrevGCID'), max_length=50, null=True, blank=False)


class BarnItem(CreatedModelMixin):
    gameinfo = models.ForeignKey(
        to='gameinfos.GameInfo',
        on_delete=models.deletion.DO_NOTHING,
        related_name='barn_items',
        db_constraint=False,
        blank=False,
        null=False,
    )
    product = models.ForeignKey(
        to='contents.Product',
        on_delete=models.deletion.DO_NOTHING,
        related_name='barn_items',
        db_constraint=False,
        blank=False,
        null=False,
    )
    amount = models.PositiveSmallIntegerField(_('amount'), null=False, blank=True, default=0)


class AbstractBuilding(CreatedModelMixin):
    bid = models.CharField(_('building id'), max_length=50, null=False, blank=False)

    class Meta:
        abstract = True


class Factory(AbstractBuilding):

    gameinfo = models.ForeignKey(
        to='gameinfos.GameInfo',
        on_delete=models.deletion.DO_NOTHING,
        related_name='factories',
        db_constraint=False,
        blank=False,
        null=False,
    )
    building = models.ForeignKey(
        to='contents.Building',
        on_delete=models.deletion.DO_NOTHING,
        related_name='factories',
        db_constraint=False,
        blank=False,
        null=False,
    )
    pos_i = models.SmallIntegerField(_('i'), null=False, blank=False)
    pos_j = models.SmallIntegerField(_('j'), null=False, blank=False)
    state = models.SmallIntegerField(_('state'), null=False, blank=False)
    check_time = models.BigIntegerField(_('check time'), null=False, blank=False)

    # 	<Upgrade version="4">
    # 		<Factory id="bakery" level="27" slx="32162038" xpBonus="65" moneyBonus="5" timeBonus="50" shelfBonus="2"/>
    # 		<Factory id="bouquetfactory" level="5" slx="32162024" xpBonus="10" timeBonus="10"/>
    level = models.PositiveSmallIntegerField(_('amount'), null=False, blank=True, default=0)
    shelf_count = models.SmallIntegerField(_('slot count'), null=False, blank=True, default=6)
    slot_count = models.SmallIntegerField(_('slot count'), null=False, blank=True, default=2)

    class Meta:
        verbose_name = 'factory'
        verbose_name_plural = 'factories'
        ordering = ['-pk']

    @property
    def products_on_shelf(self):
        now = timezone.now().astimezone(pytz.timezone('Asia/Seoul'))
        ts = time.mktime(now.timetuple())

        ret = []
        for prod in self.factory_items.order_by('idx').all():
            item_complete_time = self.check_time + prod.order_time
            if item_complete_time <= ts:
                ret.append(prod)
        return ret

    @property
    def products_on_slot(self):
        now = timezone.now().astimezone(pytz.timezone('Asia/Seoul'))
        ts = time.mktime(now.timetuple())

        ret = []
        for prod in self.factory_items.order_by('idx').all():
            item_complete_time = self.check_time + prod.order_time
            if item_complete_time > ts:
                ret.append(prod)
        return ret


class FactoryItem(CreatedModelMixin):
    factory = models.ForeignKey(
        to='gameinfos.Factory',
        on_delete=models.deletion.DO_NOTHING,
        related_name='factory_items',
        db_constraint=False,
        blank=False,
        null=False,
    )

    product = models.ForeignKey(
        to='contents.Product',
        on_delete=models.deletion.DO_NOTHING,
        related_name='factory_items',
        db_constraint=False,
        blank=False,
        null=False,
    )

    amount = models.PositiveSmallIntegerField(_('amount'), null=False, blank=False)
    idx = models.PositiveSmallIntegerField(_('amount'), null=False, blank=False)
    order_time = models.BigIntegerField(_('order time'), null=False, blank=False)
    order_max_time = models.BigIntegerField(_('order max time'), null=False, blank=False)

    class Meta:
        verbose_name = 'factory item'
        verbose_name_plural = 'factory items'
        ordering = ['-pk']


class Helicopter(AbstractBuilding):
    gameinfo = models.ForeignKey(
        to='gameinfos.GameInfo',
        on_delete=models.deletion.DO_NOTHING,
        related_name='helicopters',
        db_constraint=False,
        blank=False,
        null=False,
    )


class HelicopterItem(CreatedModelMixin):
    helicopter = models.ForeignKey(
        to='gameinfos.Helicopter',
        on_delete=models.deletion.DO_NOTHING,
        related_name='helicopter_items',
        db_constraint=False,
        blank=False,
        null=False,
    )

    product = models.ForeignKey(
        to='contents.Product',
        on_delete=models.deletion.DO_NOTHING,
        related_name='helicopter_items',
        db_constraint=False,
        blank=False,
        null=False,
    )

    amount = models.PositiveSmallIntegerField(_('amount'), null=False, blank=True, default=0)
    reward_cash = models.PositiveIntegerField(_('reward exp'), null=False, blank=False)
    reward_coin = models.PositiveIntegerField(_('reward coin'), null=False, blank=False)
    reward_exp = models.PositiveIntegerField(_('reward exp'), null=False, blank=False)


class Air(AbstractBuilding):
    gameinfo = models.ForeignKey(
        to='gameinfos.GameInfo',
        on_delete=models.deletion.DO_NOTHING,
        related_name='airs',
        db_constraint=False,
        blank=False,
        null=False,
    )


class AirItem(CreatedModelMixin):
    air = models.ForeignKey(
        to='gameinfos.Air',
        on_delete=models.deletion.DO_NOTHING,
        related_name='air_items',
        db_constraint=False,
        blank=False,
        null=False,
    )

    product = models.ForeignKey(
        to='contents.Product',
        on_delete=models.deletion.DO_NOTHING,
        related_name='air_items',
        db_constraint=False,
        blank=False,
        null=False,
    )

    amount = models.PositiveSmallIntegerField(_('amount'), null=False, blank=True, default=0)
    reward_cash = models.PositiveIntegerField(_('reward exp'), null=False, blank=False)
    reward_coin = models.PositiveIntegerField(_('reward coin'), null=False, blank=False)
    reward_exp = models.PositiveIntegerField(_('reward exp'), null=False, blank=False)


class Train(AbstractBuilding):
    gameinfo = models.ForeignKey(
        to='gameinfos.GameInfo',
        on_delete=models.deletion.DO_NOTHING,
        related_name='trains',
        db_constraint=False,
        blank=False,
        null=False,
    )

    building = models.ForeignKey(
        to='contents.Building',
        on_delete=models.deletion.DO_NOTHING,
        related_name='trains',
        db_constraint=False,
        blank=False,
        null=False,
    )