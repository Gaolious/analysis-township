from pathlib import Path
from xml.etree import ElementTree

from django.conf import settings

from app_root.contents.models import TownshipVersion, Product, Building, FactoryProduct, FactoryResource


def convert_timestring_to_seconds(t):
    multiply = {
        's': 1,
        'm': 60,
        'h': 3600,
        'd': 86400,
    }

    if isinstance(t, str):
        if t[-1] in multiply:
            len_t = len(t)
            return int(t[:len_t-1]) * multiply[ t[-1] ]
        else:
            return int(t)
    else:
        return t


def create_township_version():
    version = TownshipVersion.objects.filter(version=settings.TS_APP_VERSION).first()

    if not version:
        major, minor, patch = settings.TS_APP_VERSION.split('.')
        version = TownshipVersion.objects.create(
            version=settings.TS_APP_VERSION,
            major=major,
            minor=minor,
            patch=patch,
        )
    return version


def load_all_products_xml(version: TownshipVersion, base_path: Path):
    """
    경험치, 생산 시간, 판매 가격, 얻는 포인트, 구매 가격
    Examples>
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
    """
    filename = base_path / "All_Products.xml"

    et = ElementTree.parse(filename)
    products = et.getroot()

    bulk_list = []
    for product in products:
        product_id = product.attrib.get('id')

        if not product_id:
            continue
        if Product.objects.filter(product_id=product_id).exists():
            continue

        bulk_list.append(
            Product(
                version=version,
                build_time=convert_timestring_to_seconds(product.attrib.get('build_time')),
                exp=product.attrib.get('exp'),
                exp_on_train=product.attrib.get('expOnTrain'),
                product_id=product.attrib.get('id'),
                product_name=product.attrib.get('name'),
                level_need=product.attrib.get('levelneed'),
                max_request=product.attrib.get('maxRequest') or 0,
                reward_points_each=product.attrib.get('rewardPointsEach') or 0,
                price=product.attrib.get('price') or 0,
                sell_price=product.attrib.get('sellPrice') or 0,
                product_type=Product.get_type_from_string(product.attrib.get('type')),
                event=product.attrib.get('event', None)
            )
        )

    if bulk_list:
        Product.objects.bulk_create(
            bulk_list
        )

    return True


def load_all_material_xml(version: TownshipVersion, base_path: Path):
    """
    재료 - 판매 가격, 기차 재료시 경험치, 필요 레벨
        <mat exp="2" expOnTrain="4" icon="tntMine" id="m1" maxRequest="2" name="m1" rewardPointsEach="5" sellPrice="150" smallIcon="tntMine_small" wareMatsType="3" />
        <mat exp="1" expOnTrain="2" icon="pickaxeMine" id="m2" maxRequest="5" name="m2" rewardPointsEach="2" sellPrice="30" smallIcon="pickaxeMine_small" wareMatsType="3" />
        <mat exp="2" expOnTrain="4" icon="dynamiteMine" id="m3" maxRequest="3" name="m3" rewardPointsEach="3" sellPrice="100" smallIcon="dynamiteMine_small" wareMatsType="3" />
        <mat exp="3" expOnTrain="6" icon="products_ore_1" id="o1" maxRequest="8" name="ore_1" rewardPointsEach="1" sellPrice="8" smallIcon="ore_1_small" wareMatsType="1" />
        <mat icon="jackhammer" id="jackhammer" name="jackhammer" sellPrice="200" expOnTrain="345" smallIcon="jackhammer_small" wareMatsType="0" maxRequest="1" levelneed="60"/>
        <mat icon="powersaw" id="powersaw" name="powersaw" sellPrice="200" expOnTrain="345" smallIcon="powersaw_small" wareMatsType="0" maxRequest="1" levelneed="60"/>
        <mat icon="drill" id="drill" name="drill" sellPrice="200" expOnTrain="345" smallIcon="drill_small" wareMatsType="0" maxRequest="1" levelneed="60"/>

        <product boost="0" canBuy="0" canDonate="0" event="fishing" icon="products_eventFish2" id="eventFish2Counter" levelneed="8" maxRequest="0" name="BlueBottleCap" sellPrice="5" smallIcon="eventFish2_small" wareMatsType="0" withoutCompensation="false"/>
        <product boost="0" canBuy="0" canDonate="0" event="fishing" icon="products_eventFish3" id="eventFish3Counter" levelneed="8" maxRequest="0" name="RedBottleCap" sellPrice="6" smallIcon="eventFish3_small" wareMatsType="0" withoutCompensation="false"/>

    Parameters
    ----------
    base_path

    Returns
    -------

    """
    filename = base_path / "All_Materials.xml"

    et = ElementTree.parse(filename)
    materials = et.getroot()

    bulk_list = []
    for material in materials:
        material_id = material.attrib.get('id')

        if not material_id:
            continue
        if Product.objects.filter(product_id=material_id).exists():
            continue

        if not bool(material.get('canBuy', True)):
            continue

        bulk_list.append(
            Product(
                version=version,
                exp=material.attrib.get('exp') or 0,
                exp_on_train=material.attrib.get('expOnTrain') or 0,
                product_id=material.attrib.get('id'),
                product_name=material.attrib.get('name'),
                level_need=material.attrib.get('levelneed') or 0,
                max_request=material.attrib.get('maxRequest') or 0,
                reward_points_each=material.attrib.get('rewardPointsEach') or 0,
                price=0,
                sell_price=material.attrib.get('sellPrice') or 0,
                product_type=Product.get_type_from_string(
                    'material-{}'.format(material.attrib.get('wareMatsType'))
                ),
                event=material.attrib.get('event'),
            )
        )

    if bulk_list:
        Product.objects.bulk_create(
            bulk_list
        )

    return True


def load_all_building_xml(version: TownshipVersion, base_path: Path):

    filename = base_path / "buildings.xml"

    et = ElementTree.parse(filename)
    root = et.getroot()

    for node in root:

        if node.tag == 'livinghouse':
            """
                <livinghouse>
                    <item build_time="1m" buildingId="house26" coins_price="5" fix_price="5" icon="house26" label="house26" levelneed="4" residents="5" terrain="0,1,2"/>
                </livinghouse>
            """
            bulk_list = []
            for item in node:
                building_id = item.attrib.get('buildingId')
                if not building_id:
                    continue
                if Building.objects.filter(building_id=building_id).exists():
                    continue

                bulk_list.append(
                    Building(
                        version=version,
                        build_time=convert_timestring_to_seconds(item.attrib.get('build_time')),
                        building_id=building_id,
                        building_name=item.attrib.get('label'),
                        order_experience=0,
                        cash_price=0,
                        coins_price=item.attrib.get('coins_price'),
                        level_need=item.attrib.get('levelneed'),
                        building_type=Building.TYPE_BUILDING_HOUSE,
                        resident=item.attrib.get('residents'),
                    )
                )
            Building.objects.bulk_create(bulk_list)
        elif node.tag == 'factory':
            # 			<production>
            # 				<product amount="3" name="cowfeed" time="5m">
            # 					<resource count="2" name="wheat"/>
            # 					<resource count="1" name="corn"/>
            # 				</product>
            for item in node:
                building_id = item.attrib.get('buildingId')
                if not building_id:
                    continue
                building = Building.objects.filter(building_id=building_id).first()

                if not building:
                    building = Building.objects.create(
                            version=version,
                            build_time=convert_timestring_to_seconds(item.attrib.get('build_time')),
                            building_id=building_id,
                            building_name=item.attrib.get('label'),
                            order_experience=item.attrib.get('order_experience'),
                            cash_price=item.attrib.get('cash_price'),
                            coins_price=item.attrib.get('coins_price'),
                            level_need=item.attrib.get('levelneed'),
                            building_type=Building.TYPE_BUILDING_FACTORY,
                            resident=item.attrib.get('residents'),
                        )

                for production in item:
                    for product in production:
                        produce_amount = product.attrib.get('amount') or 1
                        produce_name = product.attrib.get('name')
                        produce_time = convert_timestring_to_seconds(product.attrib.get('time'))

                        assert 1 == Product.objects.filter(product_name=produce_name).count()
                        prod_model = Product.objects.filter(product_name=produce_name).first()

                        factory_product = FactoryProduct.objects.filter(factory=building, product=prod_model).first()
                        if not factory_product:
                            factory_product = FactoryProduct.objects.create(
                                factory=building,
                                produce_amount=produce_amount,
                                produce_time=produce_time,
                                product=prod_model,
                            )

                        resource_bulk_list = []
                        for resource in product:
                            count = resource.attrib.get('count')
                            name = resource.attrib.get('name')

                            if Product.objects.filter(product_id=name).count() == 1:
                                resource_model = Product.objects.filter(product_id=name).first()
                            elif Product.objects.filter(product_name=name).count() == 1:
                                resource_model = Product.objects.filter(product_name=name).first()
                            else:
                                raise Exception('Not found product : {}'.format(name))

                            if FactoryResource.objects.filter(product=factory_product, resource=resource_model).exists():
                                continue

                            resource_bulk_list.append(
                                FactoryResource(
                                    product=factory_product,
                                    count=count,
                                    resource=resource_model
                                )
                            )

                        if resource_bulk_list:
                            FactoryResource.objects.bulk_create(resource_bulk_list)

        elif node.tag == 'special_factory':
            # 	<special_factory>
            # 		<item build_time="2700m" buildingId="duckfactory" cash_price="0" coins_price="14500" collect_experience="0" draw="anim" label="duckfactory" levelneed="48" order_experience="2" terrain="3" volumeSize="2x2">
            # 			<production>
            # 				<product name="downFeather" time="45m"/>
            # 				<product name="bigFeather" time="120m"/>
            # 			</production>
            # 			<feeds>
            # 				<feed name="bread" time="90m">
            # 					<view>
            # 						<resource name="downFeather" min="1" max="2"/>
            # 					</view>
            # 					<slot probability="100">
            # 						<resource name="downFeather" count="1" weight="80"/>
            # 						<resource name="downFeather" count="2" weight="20"/>
            # 					</slot>
            # 				</feed>
            for item in node:
                building_id = item.attrib.get('buildingId')
                if not building_id:
                    continue
                building = Building.objects.filter(building_id=building_id).first()

                if not building:
                    building = Building.objects.create(
                            version=version,
                            build_time=convert_timestring_to_seconds(item.attrib.get('build_time')),
                            building_id=building_id,
                            building_name=item.attrib.get('label'),
                            order_experience=item.attrib.get('order_experience'),
                            cash_price=item.attrib.get('cash_price'),
                            coins_price=item.attrib.get('coins_price'),
                            level_need=item.attrib.get('levelneed'),
                            building_type=Building.TYPE_BUILDING_FACTORY,
                            resident=item.attrib.get('residents'),
                        )
                # fixme: need to implement

    return True