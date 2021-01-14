from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

"""
    models for base-contents of township
"""


class TownshipVersion(models.Model):
    version = models.CharField(_('township app version'), max_length=20, null=False, blank=False)
    major = models.PositiveSmallIntegerField(_('major version'), null=False, blank=False)
    minor = models.PositiveSmallIntegerField(_('minor version'), null=False, blank=False)
    patch = models.PositiveSmallIntegerField(_('patch version'), null=False, blank=False)

    class Meta:
        verbose_name = 'app version'
        verbose_name_plural = 'app versions'
        indexes = [
            models.Index(fields=['version'], name='idx_version'),
        ]

    def __str__(self):
        return self.version


class Product(models.Model):
    """
        <product
            build_time="2m"
            exp="1"
            expOnTrain="2" icon="seeds_wheat"
            id="wheatCounter"
            levelneed="1" maxRequest="10" name="wheat"
            price="0"
            rewardPointsEach="1"
            sellPrice="1" smallIcon="wheat_small"
            type="seed" />
    <product build_time="2m" exp="1" expOnTrain="2" icon="seeds_wheat" id="wheatCounter" levelneed="1" maxRequest="10" name="wheat" price="0" rewardPointsEach="1" sellPrice="1" smallIcon="wheat_small" type="seed" />
    <product build_time="5m" dOffX="-1" exp="1" expOnTrain="2" icon="seeds_corn" id="cornCounter" levelneed="3" maxRequest="10" name="corn" price="1" rewardPointsEach="1" sellPrice="3" smallIcon="corn_small" type="seed" />
    <product build_time="10m" exp="2" expOnTrain="4" icon="seeds_carrot" id="carrotCounter" levelneed="4" maxRequest="10" name="carrot" price="2" rewardPointsEach="1" sellPrice="5" smallIcon="carrot_small" type="seed" />
    <product boost="1" build_time="25m" canBuy="1" canDonate="1" event="thanksgiving2" exp="3" expOnTrain="6" icon="seeds_cranberry" id="cranberryCounter" levelneed="6" maxRequest="8" name="cranberry" price="3" replace="carrot" rewardPointsEach="1" sellPrice="8" smallIcon="cranberry_small" type="seed" />

    """
    TYPE_BULLION = 10
    TYPE_COINS = 20
    TYPE_FEED = 30
    TYPE_FRUIT = 40
    TYPE_PRODUCT = 50
    TYPE_SEED = 60
    TYPE_MATERIAL_0 = 100
    TYPE_MATERIAL_1 = 110
    TYPE_MATERIAL_2 = 120
    TYPE_MATERIAL_3 = 130
    TYPE_MATERIAL_4 = 140
    TYPE_MATERIAL_5 = 150
    TYPE_MATERIAL_6 = 160
    TYPE_MATERIAL_7 = 170
    TYPE_MATERIAL_8 = 180
    CHOICE_TYPE = (
        (TYPE_BULLION, 'bullion'),
        (TYPE_COINS, 'coins'),
        (TYPE_FEED, 'feed'),
        (TYPE_FRUIT, 'fruit'),
        (TYPE_PRODUCT, 'product'),
        (TYPE_SEED, 'seed'),
        (TYPE_MATERIAL_0, 'material-0'),
        (TYPE_MATERIAL_1, 'material-1'),
        (TYPE_MATERIAL_2, 'material-2'),
        (TYPE_MATERIAL_3, 'material-3'),
        (TYPE_MATERIAL_4, 'material-4'),
        (TYPE_MATERIAL_5, 'material-5'),
        (TYPE_MATERIAL_6, 'material-6'),
        (TYPE_MATERIAL_7, 'material-7'),
        (TYPE_MATERIAL_8, 'material-8'),
    )
    version = models.ForeignKey(
        to='contents.TownshipVersion',
        on_delete=models.deletion.DO_NOTHING,
        related_name='products',
        db_constraint=False,
        blank=False,
        null=False,
    )
    # build time in seconds
    build_time = models.PositiveIntegerField(_('build time'), null=True, blank=False, default=None)

    exp = models.PositiveIntegerField(_('exp'), null=False, blank=False)

    exp_on_train = models.PositiveIntegerField(_('exp on train'), null=False, blank=False)

    product_id = models.CharField(_('product id'), max_length=50, unique=True, null=False, blank=False)

    product_name = models.CharField(_('product name'), max_length=50, null=False, blank=False)

    level_need = models.PositiveIntegerField(_('level need'), null=False, blank=False)

    max_request = models.PositiveIntegerField(_('max request'), blank=False, default=None)

    reward_points_each = models.PositiveIntegerField(_('reward points each'), blank=False, default=None)

    price = models.PositiveIntegerField(_('price'), blank=False, default=None)

    sell_price = models.PositiveIntegerField(_('sell price'), blank=False, default=None)

    product_type = models.SmallIntegerField(_('product type'), choices=CHOICE_TYPE, null=False, blank=False)

    event = models.CharField(_('event'), max_length=50, null=True, blank=False)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

        indexes = [
            models.Index(fields=['product_name'], name='idx_product_name'),
            models.Index(fields=['product_type'], name='idx_product_type'),
        ]

    @classmethod
    def get_type_from_string(cls, s:str):
        for a in cls.CHOICE_TYPE:
            if a[1] == s:
                return a[0]
        return None

    def __str__(self):
        return self.product_name

    @property
    def url(self):
        return '{}images/{}/{}.png'.format(
            settings.STATIC_URL,
            self.get_product_type_display(),
            self.product_name,
        )

    @property
    def is_event(self):
        return self.event is not None

    @property
    def is_product(self):
        return self.product_type == self.TYPE_PRODUCT

    @property
    def is_seed(self):
        return self.product_type == self.TYPE_SEED


class Building(models.Model):
    TYPE_BUILDING_HOUSE = 10
    TYPE_BUILDING_FACTORY = 20
    TYPE_BUILDING_SPECIAL_FACTORY = 30

    CHOICE_TYPE_BUILDING = (
        (TYPE_BUILDING_HOUSE, _('house')),
        (TYPE_BUILDING_FACTORY, _('factory')),
        (TYPE_BUILDING_SPECIAL_FACTORY, _('special factory')),
    )

    version = models.ForeignKey(
        to='contents.TownshipVersion',
        on_delete=models.deletion.DO_NOTHING,
        related_name='buildings',
        db_constraint=False,
        blank=False,
        null=False,
    )

    # build time in seconds
    build_time = models.PositiveIntegerField(_('build time'), null=True, blank=False, default=None)

    building_id = models.CharField(_('building id'), max_length=50, null=False, blank=False)

    building_name = models.CharField(_('building name'), max_length=50, null=False, blank=False)

    order_experience = models.PositiveIntegerField(_('cash price'), null=True, blank=False, default=None)

    cash_price = models.PositiveIntegerField(_('cash price'), null=True, blank=False, default=None)

    coins_price = models.PositiveIntegerField(_('coins price'), null=True, blank=False, default=None)

    level_need = models.PositiveIntegerField(_('level need'), null=True, blank=False, default=None)

    building_type = models.PositiveSmallIntegerField(_('building type'), choices=CHOICE_TYPE_BUILDING, null=False, blank=False)

    resident = models.PositiveIntegerField(_('resident'), null=True, blank=False, default=None)  # house only

    @property
    def is_house(self):
        return self.building_type == self.TYPE_BUILDING_HOUSE

    @property
    def is_factory(self):
        return self.building_type == self.TYPE_BUILDING_FACTORY

    @property
    def is_special_factory(self):
        return self.building_type == self.TYPE_BUILDING_SPECIAL_FACTORY

    class Meta:
        verbose_name = 'building'
        verbose_name_plural = 'buildings'

    def __str__(self):
        return self.building_name


class FactoryProduct(models.Model):
    """
        <production>
            <product amount="3" name="cowfeed" time="5m">
                <resource count="2" name="wheat"/>
                <resource count="1" name="corn"/>
            </product>
    """
    factory = models.ForeignKey(
        to='contents.Building',
        on_delete=models.deletion.DO_NOTHING,
        related_name='factory_products',
        db_constraint=False,
        blank=False,
        null=False,
    )

    produce_amount = models.PositiveIntegerField(_('produce amount'), null=False, blank=False)
    produce_time = models.PositiveIntegerField(_('produce time'), null=False, blank=False)

    product = models.ForeignKey(
        to='contents.Product',
        on_delete=models.deletion.DO_NOTHING,
        related_name='factory_products',
        db_constraint=False,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'factory_product'
        verbose_name_plural = 'factory_products'

    def __str__(self):
        return 'Building[{}]: Product[{}]'.format(
            self.factory.building_name,
            self.product.product_name
        )

class FactoryResource(models.Model):
    """
        <production>
            <product amount="3" name="cowfeed" time="5m">
                <resource count="2" name="wheat"/>        <--------
                <resource count="1" name="corn"/>
            </product>
    """
    product = models.ForeignKey(
        to='contents.FactoryProduct',
        on_delete=models.deletion.DO_NOTHING,
        related_name='factory_resources',
        db_constraint=False,
        blank=False,
        null=False,
    )
    count = models.PositiveIntegerField(_('number of products'), null=False, blank=False)

    resource = models.ForeignKey(
        to='contents.Product',
        on_delete=models.deletion.DO_NOTHING,
        related_name='factory_resources',
        db_constraint=False,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'factory_resource'
        verbose_name_plural = 'factory_resources'

    def __str__(self):
        return '{}: Res[{}] / {}'.format(
            self.product,
            self.resource,
            self.count,
        )