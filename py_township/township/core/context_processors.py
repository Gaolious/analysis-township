# -*- coding:utf-8 -*-
from django.conf import settings
from django.urls import reverse_lazy


class AbstractMenu(object):
    display_name = None
    link = None
    key = None
    child_menus = []
    fa_icon = None

    def __init__(self, key, display_name, link=None, fa_icon='chart-area'):
        self.child_menus = []
        self.key = key
        self.display_name = display_name
        self.link = link
        self.fa_icon = fa_icon

    @property
    def has_child(self):
        return True if self.child_menus else False

    def add_child(self, *args):
        for menu in args:
            self.child_menus.append(menu)
            menu.parent = self

    @property
    def childs(self):
        for c in self.child_menus:
            yield c

    @property
    def icon_name(self):
        return 'fa-{}'.format(self.fa_icon)


class MenuCategory(AbstractMenu):
    pass


class MenuGroup(AbstractMenu):
    pass


class MenuItem(AbstractMenu):
    pass


def add_helper_category():
    cate_helper = MenuCategory(key='cate_helper', display_name='Helper')

    grp_hex2bin = MenuGroup(key='grp_hex2bin', display_name='HexDump TO Binary', link=reverse_lazy('app_root:helpers:hex2bin'))

    grp_base64 = MenuGroup(key='grp_base64', display_name='Base64 Enc/Dec', link=reverse_lazy('app_root:helpers:base64'))

    grp_gzip = MenuGroup(key='grp_gzip', display_name='Gzip Enc/Dec', link=reverse_lazy('app_root:helpers:gzip'))

    grp_flow = MenuGroup(key='grp_flow', display_name='Flows')

    item_fetch_data = MenuItem(key='item_fetch_data', display_name='Fetch Data', link=reverse_lazy('app_root:helpers:flow_fetch_data'))
    item_fetch_city = MenuItem(key='item_fetch_city', display_name='Fetch City', link=reverse_lazy('app_root:helpers:flow_fetch_city'))
    grp_flow.add_child(item_fetch_data, item_fetch_city)

    grp_decode = MenuGroup(key='cate_decode', display_name='Decode Signature')

    item_0x54 = MenuItem(key='0x54', display_name='0x54')
    item_0x53 = MenuItem(key='0x53', display_name='0x53')
    item_0x78 = MenuItem(key='0x78', display_name='0x78')
    item_0x79 = MenuItem(key='0x79', display_name='0x79')
    item_0x64 = MenuItem(key='0x64', display_name='0x64')
    item_0x66 = MenuItem(key='0x66', display_name='0x66')
    item_0x6F = MenuItem(key='0x6F', display_name='0x6F')
    item_0x1F8B = MenuItem(key='0x8b1f', display_name='0x1F 0x8B')
    item_0x504c5845 = MenuItem(key='0x45584c50', display_name='0x50 0x4c 0x58 0x45')

    grp_decode.add_child(
        item_0x54,
        item_0x53,
        item_0x78,
        item_0x79,
        item_0x64,
        item_0x66,
        item_0x6F,
        item_0x1F8B,
        item_0x504c5845,
    )
    
    cate_helper.add_child(grp_hex2bin, grp_base64, grp_gzip, grp_flow, grp_decode)
    return cate_helper


def add_search_category():
    cate_search = MenuCategory(key='cate_search', display_name='Search')
    grp_keywords = MenuGroup(key='grp_keywords', display_name='Keyword List', link=reverse_lazy('app_root:keywords:first'))
    cate_search.add_child(grp_keywords)
    return cate_search


def add_gameinfo_category():
    cate_game_data = MenuCategory(key='cate_game_data', display_name='Game Data')

    grp_bot = MenuGroup(key='grp_game_info', display_name='TS Bot', link=reverse_lazy('app_root:gameinfos:list'))
    grp_game_info = MenuGroup(key='grp_game_info', display_name='Request Analysis', link=reverse_lazy('app_root:analysis:list'))

    cate_game_data.add_child(grp_bot, grp_game_info)
    return cate_game_data


def admin_menu(request):

    return {
        'admin_menu': [
            add_helper_category(),
            add_gameinfo_category(),
            add_search_category(),
        ]
    }
