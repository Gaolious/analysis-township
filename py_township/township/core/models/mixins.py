from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class CreatedModelMixin(models.Model):
    create_at = models.DateTimeField(_('create'), null=False, blank=True, default=timezone.now)
    update_at = models.DateTimeField(_('update'), null=False, blank=True, default=timezone.now)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        now = timezone.now()
        if self.pk is None:
            self.created = now

        self.update_at = now

        if isinstance(update_fields, list):
            update_fields.append('update_at')

        super(CreatedModelMixin, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )