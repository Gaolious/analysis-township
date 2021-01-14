import copy
import json
from typing import List
from xml.etree import ElementTree

from django.urls import reverse_lazy
from django.views import generic

from app_root.analysis.forms import AnalysisForm
from app_root.analysis.models import RequestSaveCity

CURRENT_MENU = 'analysis'


class RequestSaveCityListView(generic.ListView):
    model = RequestSaveCity
    template_name = 'analysis_list.html'


class RequestSaveCityCreateView(generic.CreateView):
    active_side_menu = CURRENT_MENU
    form_class = AnalysisForm
    model = RequestSaveCity
    template_name = 'analysis_create.html'


class RequestSaveCityDetailView(generic.DetailView):
    active_side_menu = CURRENT_MENU
    model = RequestSaveCity
    template_name = 'analysis_detail.html'
    pk_url_kwarg = 'analysis_pk'


class XmlNode(object):
    tag: str = None
    attrs: dict = {}
    childs: List = []

    def __init__(self):
        self.attrs = {}
        self.childs = []

    @staticmethod
    def parse(node: ElementTree.Element):
        obj = XmlNode()
        obj.tag = node.tag

        if node.attrib:
            obj.attrs = copy.deepcopy(node.attrib)
        for c in node:
            obj.childs.append(XmlNode.parse(node=c))
        return obj

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

    def find_child_idx(self, tag, attr):

        for i in range(len(self.childs)):
            c = self.childs[i]
            if c.tag == tag and c.attrs == attr:
                return i
        return None

    def remove_equal_node(self, other):

        equal_tag = self.tag == other.tag
        equal_attr = self.attrs == other.attrs

        del_idx_list = []

        for i in range(len(self.childs)):
            c = self.childs[i]

            idx = other.find_child_idx(c.tag, c.attrs)
            if idx is None:
                continue

            if c.remove_equal_node(other=other.childs[idx]):
                del other.childs[idx]
                del_idx_list.append(i)

        for i in reversed(del_idx_list):
            del self.childs[i]

        if len(self.childs) == 0 and len(other.childs) == 0 and equal_attr and equal_tag:
            return True
        else:
            return False


class RequestSaveCityDiffView(generic.TemplateView):
    active_side_menu = CURRENT_MENU
    template_name = 'analysis_diff.html'

    def get_context_data(self, **kwargs):
        ctx = super(RequestSaveCityDiffView, self).get_context_data(**kwargs)
        pk1 = self.request.GET.get('p1')
        pk2 = self.request.GET.get('p2')

        obj1: RequestSaveCity = RequestSaveCity.objects.filter(pk=pk1).first()
        obj2: RequestSaveCity = RequestSaveCity.objects.filter(pk=pk2).first()

        root1 = ElementTree.fromstring(obj1.xml_data)
        root2 = ElementTree.fromstring(obj2.xml_data)

        node1 = XmlNode.parse(node=root1)
        node2 = XmlNode.parse(node=root2)
        node1.remove_equal_node(node2)

        ctx.update({
            'title1': pk1,
            'title2': pk2,
            'json1': json.loads(obj1.json_data),
            'json2': json.loads(obj2.json_data),
            'node1': '\n'.join(node1.get_xml_string(0)),
            'node2': '\n'.join(node2.get_xml_string(0)),
        })
        return ctx
