import typing

from django.db import models

from core.utils import hash10


class KeywordManager(models.Manager):

    def with_encoded_keyword(self, encoded_keyword):

        if isinstance(encoded_keyword, (bytes, bytearray)):
            encoded_keyword = encoded_keyword.hex()

        return self.filter(
            encoded_hash=hash10(encoded_keyword),
            encoded_hex_string=encoded_keyword
        )


class Keyword(models.Model):
    # segment base = 0x00000000
    address = models.BigIntegerField('address', db_index=True, null=False, blank=False)

    encoded_hex_string = models.CharField('encoded hex string', max_length=400, null=False, blank=False)
    encoded_hash = models.BigIntegerField('encoded string', null=False, db_index=True)

    decoded_string = models.CharField('decoded string', max_length=200, null=False, blank=False)
    decoded_hash = models.BigIntegerField('decoded string', null=False, db_index=True)

    objects = KeywordManager()

    class Meta:
        verbose_name = 'keyword'
        verbose_name_plural = 'keywords'

        ordering = ['pk']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        encoded_hash = hash10(self.encoded_hex_string)
        decoded_hash = hash10(self.decoded_string)

        if self.encoded_hash != encoded_hash:
            self.encoded_hash = encoded_hash
            if isinstance(update_fields, (list, set)):
                update_fields.append('encoded_hash')

        if self.decoded_hash != decoded_hash:
            self.decoded_hash = decoded_hash
            if isinstance(update_fields, (list, set)):
                update_fields.append('decoded_hash')

        return super(Keyword, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
