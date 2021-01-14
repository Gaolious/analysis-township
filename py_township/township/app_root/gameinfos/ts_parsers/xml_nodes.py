import copy
import json
import random
from typing import List, Dict
from xml.etree import ElementTree


class AbstractNode(object):
    tag: str = None
    attrs: dict = {}
    childs: List = []

    def __init__(self):
        self.attrs = {}
        self.childs = []

    def update_timestamp(self, ts):
        pass

    def parse(self, node: ElementTree.Element):
        self.tag = node.tag

        if node.attrib:
            self.attrs = copy.deepcopy(node.attrib)

            for k in self.attrs:
                if isinstance(self.attrs[k], str) and len(self.attrs[k]) > 2 and self.attrs[k][0] == '{' and self.attrs[k][-1] == '}':
                    try:
                        d = json.loads(self.attrs[k])
                        self.attrs[k] = d
                    except Exception as e:
                        pass
        for c in node:
            obj = AbstractNode()
            obj.parse(c)
            self.childs.append(obj)

    @property
    def xml_attr_string(self):
        attr_list = []
        for att in self.attrs:

            val = self.attrs[att]
            if isinstance(val, dict):
                val = json.dumps(val, separators=(',', ':'))
            elif isinstance(val, bool):
                val = '1' if val else '0'
            else:
                val = str(val)

            if val:
                val = val.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

            if "'" in val and '"' in val:
                attr_list.append("{}='{}'".format(att, val.replace("'", "&apos;")))
            elif '"' in val:
                attr_list.append("{}='{}'".format(att, val))
            else:
                attr_list.append('{}="{}"'.format(att, val))

        return ' '.join(attr_list)

    def get_xml_string(self, depth=0):
        tab = '\t' * depth
        ret = []
        attr_string = self.xml_attr_string
        if self.childs:
            if attr_string:
                ret.append('{}<{} {}>'.format(tab, self.tag, attr_string))
            else:
                ret.append('{}<{}>'.format(tab, self.tag))
            for child in self.childs:
                ret += child.get_xml_string(depth=depth+1)
            ret.append('{}</{}>'.format(tab, self.tag))
        else:
            if attr_string:
                ret.append('{}<{} {}/>'.format(tab, self.tag, attr_string))
            else:
                ret.append('{}<{}/>'.format(tab, self.tag))

        return ret


class Vars(AbstractNode):

    @property
    def name(self):
        return self.attrs.get('name')


class GlobalNode(AbstractNode):
    tag = 'Global'

    child_dict = {}

    def __init__(self):
        super(GlobalNode, self).__init__()

    def parse(self, node: ElementTree.Element):
        self.tag = node.tag

        if node.attrib:
            self.attrs = copy.deepcopy(node.attrib)
        for c in node:
            obj = Vars()
            obj.parse(c)
            self.child_dict.update({obj.name.lower(): obj})

    def get_xml_string(self, depth=0):
        tab = '\t' * depth
        ret = []
        attr_string = self.xml_attr_string

        if self.child_dict:
            if attr_string:
                ret.append('{}<{} {}>'.format(tab, self.tag, attr_string))
            else:
                ret.append('{}<{}>'.format(tab, self.tag))

            for name in self.child_dict:
                child = self.child_dict.get(name)
                ret += child.get_xml_string(depth=depth+1)
            ret.append('{}</{}>'.format(tab, self.tag))
        else:
            if attr_string:
                ret.append('{}<{} {}/>'.format(tab, self.tag, attr_string))
            else:
                ret.append('{}<{}/>'.format(tab, self.tag))

        return ret

    def get_attr_value(self, key: str):
        key = key.lower()

        if key in self.child_dict:
            if self.child_dict[key].attrs.get('t') == 'i':
                return int(self.child_dict[key].attrs['v'])
            elif self.child_dict[key].attrs.get('t') == 'b':
                return bool(self.child_dict[key].attrs['v'])
            elif self.child_dict[key].attrs.get('t') == 'f':
                return float(self.child_dict[key].attrs['v'])
            else:
                return self.child_dict[key].attrs['v']

        return None

    def update_timestamp(self, ts):
        """
            <Globals>
                <Var name="saveGlobalTime" v="1609168504" t="i"/>
                <Var name="factoryTime" v="1609168504" t="i"/>
                <Var name="VCheckTime" v="1609168504" t="i"/>
            </Globals>
        """
        ##################################################################################
        # save Global Time, factory Time, VCheck Time
        ##################################################################################
        keys = [
            'saveGlobalTime',
            'factoryTime',
            'VCheckTime',
        ]
        for k in keys:
            k = k.lower()
            self.child_dict[k].attrs['v'] = ts
        ##################################################################################
        # CTTime, SCTime
        ##################################################################################
        keys = [
            'CTTime',
            'SCTime'
        ]
        new_ts = ts - random.randint(1, 2)
        for k in keys:
            k = k.lower()
            self.child_dict[k].attrs['v'] = new_ts

        ##################################################################################
        # time in Game
        ##################################################################################
        k = 'timeInGame'.lower()
        timeInGame_sec, timeInGame_nsec = self.child_dict[k].attrs['v'].split('.')

        timeInGame_sec = int(timeInGame_sec) + random.randint(5, 15)
        timeInGame_nsec = (int(timeInGame_nsec) // 10000000) + random.randint(10000000, 99999999)
        timeInGame_nsec = timeInGame_nsec % 100000000

        self.child_dict[k].attrs['v'] = '{0:d}.{1:09d}0000000'.format(timeInGame_sec, timeInGame_nsec)



class BuildingObject(AbstractNode):
    tag = 'Object'

    def parse(self, node: ElementTree.Element):
        super(BuildingObject, self).parse(node)

    def get_store_id(self):
        return self.attrs.get('data', {}).get('storeId')

    def update_timestamp(self, ts):
        if 'data' in self.attrs and 'time' in self.attrs['data']:
            self.attrs['data']['time'] = ts


class BuildingsNode(AbstractNode):
    tag = 'Buildings'

    child_dict: Dict[str, List[BuildingObject]] = {}

    def draw_map(self, node: ElementTree.Element):
        sx, ex = 0, 80
        sy, ey = 0, 80

        min_y = 9999
        min_x = 9999
        max_y = 0
        max_x = 0
        storeId_list = set([])

        map_data = [[0]*80 for i in range(80)]

        for c in node:
            data = json.loads(c.attrib['data'])
            x = data['i']
            y = data['j']
            storeId = data['storeId']

            max_y = max(max_y, y)
            max_x = max(max_x, x)

            min_y = min(min_y, y)
            min_x = min(min_x, x)

            storeId_list.add(storeId)
            map_data[y][x] = storeId

        print("({}, {}) ~ ({}, {})".format(min_y, min_x, max_y, max_x))
        print(storeId_list)

        for y in range(max_y):

            if y == 0:
                s = []
                for x in range(max_x):
                    if sx <= x <= ex and sy <= y <= ey:
                        s.append('{0:30d}'.format(x))
                print(' '.join(s))

            s = ['{0:30d}'.format(y)]

            for x in range(max_x):
                if sx <= x <= ex and sy <= y <= ey:
                    c = map_data[y][x]
                    s.append(' '*30 if c == 0 else c[:30])

            print(' '.join(s))

    def parse(self, node: ElementTree.Element):
        self.tag = node.tag

        if node.attrib:
            self.attrs = copy.deepcopy(node.attrib)
        for c in node:
            obj = BuildingObject()
            obj.parse(c)
            key = obj.get_store_id()

            if key not in self.child_dict:
                self.child_dict.update({key: []})
            self.child_dict[key].append(obj)

    def get_xml_string(self, depth=0):
        tab = '\t' * depth
        ret = []
        attr_string = self.xml_attr_string

        if self.child_dict:
            if attr_string:
                ret.append('{}<{} {}>'.format(tab, self.tag, attr_string))
            else:
                ret.append('{}<{}>'.format(tab, self.tag))

            for name in self.child_dict:
                for child in self.child_dict.get(name):
                    ret += child.get_xml_string(depth=depth+1)
            ret.append('{}</{}>'.format(tab, self.tag))
        else:
            if attr_string:
                ret.append('{}<{} {}/>'.format(tab, self.tag, attr_string))
            else:
                ret.append('{}<{}/>'.format(tab, self.tag))

        return ret

    def get_buildings_by_id(self, building_id):
        return self.child_dict.get(building_id, [])

    def update_timestamp(self, ts):
        for k in self.child_dict:
            for node in self.child_dict[k]:
                node.update_timestamp(ts)


class DevicesNode(AbstractNode):

    def update_timestamp(self, ts):
        for child in self.childs:
            if 't' in child.attrs:
                child.attrs['t'] = ts


class TrainSubNode(AbstractNode):
    pass


class TrainNode(AbstractNode):
    pass


class EtcNode(AbstractNode):
    pass
