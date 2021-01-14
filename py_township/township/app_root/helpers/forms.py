import base64
from functools import cached_property
from typing import Union, Optional

from django import forms

from modules.ts_utils import hex_dump_to_bytes
from modules.ts_gzip import ts_uncompress, ts_compress


class AbstractHelperForm(forms.Form):

    def bytes(self):
        raise NotImplementedError('You should implement this function')

    @cached_property
    def get_bytes(self) -> Optional[bytearray]:
        return self.bytes()

    @cached_property
    def get_hex_string(self) -> Optional[str]:
        b = self.get_bytes
        return b.hex() if b else None

    @cached_property
    def get_const_char(self) -> Optional[str]:
        b = self.get_bytes
        return ''.join(["\\x{:02x}".format(a) for a in b]) if b else None

    @cached_property
    def get_base64(self) -> Optional[bytes]:
        b = self.get_bytes
        return base64.b64encode(b).decode('utf-8') if b else None

    @cached_property
    def hex_dump(self) -> Optional[str]:
        b = self.get_bytes
        if b:
            lines = []
            length = len(b)
            for i in range(0, length, 16):
                lines.append(' '.join(['{:02x}'.format( b[j] ) for j in range(i, min(length, i+16))]))
            return '\n'.join(lines)
        else:
            return None


class HexToBinaryForm(AbstractHelperForm):

    hex_string = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    is_include_address = forms.TypedChoiceField(
        label='involving address ?',
        initial=True,
        required=True,
        coerce=lambda x: x == 'True',
        choices=(
            (True, 'True'),
            (False, 'False')
        ),
        widget=forms.RadioSelect
    )

    number_of_bytes = forms.CharField(
        label='number of bytes',
        initial=0,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def bytes(self):
        if hasattr(self, 'cleaned_data') and 'hex_string' in self.cleaned_data:
            lines = [a.strip() for a in self.cleaned_data.get('hex_string', '').splitlines() if a.strip()]
            is_included_address = self.cleaned_data.get('is_include_address', True)
            number_of_bytes = self.cleaned_data.get('number_of_bytes', '')

            address_pos = 0
            hex_pos = 0
            printable_pos = 0
            if lines:
                if is_included_address:
                    hex_pos = lines[0].index(' ', address_pos)
                    while hex_pos < len(lines[0]) and lines[0][hex_pos] == ' ':
                        hex_pos += 1

                printable_pos = hex_pos + 1

                for i in range(16):
                    t = lines[0].index(' ', printable_pos)
                    if t < 0:
                        printable_pos = -1
                    else:
                        printable_pos = t + 1

                if hex_pos >= 0 and hex_pos < printable_pos:
                    for i in range(len(lines)):
                        lines[i] = lines[i][hex_pos:printable_pos].strip()

            ret = bytearray([])

            count = len(lines)
            for i in range(count):
                arr = [a.strip() for a in lines[i].split(' ') if a.strip()]
                ret += bytearray.fromhex(''.join(arr))

            if number_of_bytes:
                try:
                    if number_of_bytes.startswith('0x'):
                        number_of_bytes = int(number_of_bytes, 16)
                    else:
                        number_of_bytes = int(number_of_bytes, 10)
                except:
                    try:
                        number_of_bytes = int(number_of_bytes, 16)
                    except:
                        number_of_bytes = 0

            if number_of_bytes and number_of_bytes > 0:
                return ret[:number_of_bytes]
            return ret
        return None


class Base64EncodeDecodeForm(AbstractHelperForm):

    CHOICE_KIND_BASE64 = 1
    CHOICE_KIND_BASE66 = 2
    CHOICE_KIND = (
        (CHOICE_KIND_BASE64, 'base64'),
        (CHOICE_KIND_BASE66, 'base66'),
    )

    data = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    kind = forms.TypedChoiceField(
        label='Kind of base64',
        initial=CHOICE_KIND_BASE64,
        required=True,
        choices=CHOICE_KIND,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def bytes(self):
        if hasattr(self, 'cleaned_data') and 'data' in self.cleaned_data:
            return base64.b64decode(
                self.cleaned_data['data']
            )
        return None


class GzipCompressUncompressForm(AbstractHelperForm):

    CHOICE_KIND_HEX_STRING = 1
    CHOICE_KIND_HEX_DUMP = 2
    CHOICE_KIND = (
        (CHOICE_KIND_HEX_STRING, 'Hex String'),
        (CHOICE_KIND_HEX_DUMP, 'Hex Dump'),
    )

    CHOICE_MODE_COMPRESS = 1
    CHOICE_MODE_UNCOMPRESS = 2
    CHOICE_MODE = (
        (CHOICE_MODE_COMPRESS, 'compress'),
        (CHOICE_MODE_UNCOMPRESS, 'uncompress'),
    )

    data = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    mode = forms.TypedChoiceField(
        label='입력 종류',
        initial=CHOICE_KIND_HEX_STRING,
        required=True,
        choices=CHOICE_MODE,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    kind = forms.TypedChoiceField(
        label='kind',
        initial=CHOICE_MODE_UNCOMPRESS,
        required=True,
        choices=CHOICE_KIND,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    is_include_address = forms.TypedChoiceField(
        label='involving address ?',
        initial=False,
        required=True,
        coerce=lambda x: x == 'True',
        choices=(
            (True, 'True'),
            (False, 'False')
        ),
        widget=forms.RadioSelect
    )

    def bytes(self):
        if hasattr(self, 'cleaned_data') and 'data' in self.cleaned_data:
            data = self.cleaned_data['data']
            is_included_address = self.cleaned_data['is_include_address']
            mode = int(self.cleaned_data['mode'])
            kind = int(self.cleaned_data['kind'])

            ret = bytearray([])

            if kind == self.CHOICE_KIND_HEX_STRING:
                data = data.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
                ret = bytearray.fromhex(data)
            else:
                lines = [a for a in data.splitlines() if a.strip()]
                count = len(lines)
                for i in range(count):
                    arr = [a for a in lines[i].split(' ') if a.strip()]
                    s = 1 if is_included_address else 0

                    ret += bytearray.fromhex(''.join(arr[s:])[:32])

            if mode == self.CHOICE_MODE_UNCOMPRESS:
                return ts_uncompress(ret)
            else:
                return ts_compress(ret)

        return None
