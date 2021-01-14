
from django import forms

from app_root.analysis.models import RequestSaveCity


class AnalysisForm(forms.ModelForm):

    hex_string = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    ts_id = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    memo = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = RequestSaveCity

        fields = (
            'ts_id',
            'memo'
        )

    def save(self, commit=True):
        import base64
        import json
        from modules.ts_aes import ts_aes_decode_with_tsid
        from modules.ts_gzip import ts_uncompress
        from modules.ts_file import ts_decode_bytearray

        data = bytearray.fromhex(self.cleaned_data['hex_string'])
        
        self.instance.size = len(data)

        decoded_body = ts_aes_decode_with_tsid(body=data, ts_id=self.cleaned_data['ts_id'])
        uncompress_body = ts_uncompress(decoded_body)

        json_body = json.loads(uncompress_body, strict=False)
        result_data = json_body.pop('data', None)

        self.instance.json_data = json.dumps(json_body).encode('utf-8')

        if result_data:

            result_data = bytearray(base64.b64decode(result_data))

            result_data = ts_uncompress(
                ts_decode_bytearray(result_data, len(result_data))
            )

            self.instance.xml_data = result_data
        else:
            self.instance.xml_data = bytes([])
        
        return super(AnalysisForm, self).save(commit=commit)