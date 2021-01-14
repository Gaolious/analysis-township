from django.views import generic

from app_root.helpers.forms import HexToBinaryForm, Base64EncodeDecodeForm, GzipCompressUncompressForm
from app_root.keywords.models import Keyword

CURRENT_MENU = 'dashboard'

class AbstractHelperView(generic.FormView):
    active_side_menu = CURRENT_MENU

    def get(self, request, *args, **kwargs):
        return super(AbstractHelperView, self).get(request=request, args=args, kwargs=kwargs)

    def form_valid(self, form):
        ctx = self.get_context_data()
        ctx.update({
            'form': form
        })
        return self.render_to_response(ctx)


class HexToBinaryView(AbstractHelperView):
    """

A732CB80  79 F7 5C 10 7F F3 4D E0  5F EF BE 56 77 C2 33 6D  y...........w..m
A732CB90  80 20 11 AF 2E 16 4C B7  CF 28 37 23 EE 3E BD 7A  . ....L...7#...z
A732CBA0  99 1E ED FD 41 CE 64 8C  4B 30 87 5F C2 8D 0E 96  ........K0._....
A732CBB0  9E 37 27 A6 12 5F 0F 60  E7 4A A5 EE 4D 9A 77 4E  .7'.._.`......wN
A732CBC0  D3 50 54 6B 52 D2 28 2E  B4 79 78 C1 A5 29 84 7A  ..TkR....yx..).z
A732CBD0  E3 F4 15 25 FD 65 51 92  23 D1 4D AB 1C 65 71 AE  ...%.eQ.#....eq.
A732CBE0  1B 37 22 D3 06 9F 6C D8  44 5D 3A 11 55 E7 34 60  .7"...l..]:.U...
A732CBF0  7A FC 84 43 E2 42 2D D7  47 B4 7C 68 CD 2C B6 2F  z..C......|h.../

을 binary 파일로 생성.
    """
    template_name = 'hex_to_binary.html'
    form_class = HexToBinaryForm


class Base64EncodeDecodeView(AbstractHelperView):
    """
    base64 encode/decode
    """
    template_name = 'base64.html'
    form_class = Base64EncodeDecodeForm


class GzipCompressUncompressView(AbstractHelperView):
    """
    base64 encode/decode
    """
    template_name = 'gzip.html'
    form_class = GzipCompressUncompressForm


class FlowView_fetch_data(generic.TemplateView):
    template_name = 'flow-fetch_data.html'


class FlowView_fetch_city(generic.TemplateView):
    template_name = 'flow-fetch_city.html'