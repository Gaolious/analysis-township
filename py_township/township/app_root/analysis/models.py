import json

from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from core.models.mixins import CreatedModelMixin


class RequestSaveCity(CreatedModelMixin):
    json_data = models.BinaryField(_('json data'), max_length=10000, null=False, blank=False)
    xml_data = models.BinaryField(_('xml data'), max_length=1000000, null=False, blank=False)
    ts_id = models.CharField(_('ts-id'), max_length=100, null=False, blank=False)
    size = models.PositiveIntegerField(_('size'), null=False, blank=False)
    memo = models.CharField(_('memo'), max_length=200, null=False, blank=False)

    class Meta:
        verbose_name = 'Request Save City'
        verbose_name_plural = 'Request Save City'

        ordering = ['-pk']

    def get_absolute_url(self):
        return reverse_lazy(
            viewname='app_root:analysis:detail',
            kwargs={
                'analysis_pk': self.pk
            }
        )

    def get_json_data(self):
        data = json.loads(self.json_data, strict=False)

        return data

    def get_xml_data(self):
        return self.xml_data.decode('utf-8')