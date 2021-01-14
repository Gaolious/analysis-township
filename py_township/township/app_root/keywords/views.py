from django.db.models import Q
from django.views import generic

from app_root.helpers.forms import HexToBinaryForm
from app_root.keywords.models import Keyword
from core.utils import hash10
from core.views.mixins import CursorPaginationMixin

CURRENT_MENU = 'dashboard'


class KeywordView(CursorPaginationMixin):
    active_side_menu = CURRENT_MENU
    template_name = 'keyword_list.html'
    model = Keyword
    paginate_by = 20
    search_keyword = None

    def __init__(self):
        super(KeywordView, self).__init__()
        self.search_keyword = None

    def is_hexdigit_keyword(self):
        try:
            return int(self.search_keyword, 16) >= 0
        except:
            return False

    def is_decimal_keyword(self):
        try:
            return int(self.search_keyword, 10) >= 0
        except:
            return False

    def get_queryset(self):
        queryset = super(KeywordView, self).get_queryset()

        if self.search_keyword:
            queryset = queryset.filter(
                Q(encoded_hex_string__startswith=self.search_keyword) |
                Q(decoded_string__startswith=self.search_keyword)
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(KeywordView, self).get_context_data(object_list=object_list, kwargs=kwargs)
        if self.search_keyword:
            ctx.update({
                'search_keyword': self.search_keyword
            })
        return ctx

    def get(self, request, *args, **kwargs):
        if 'search_keyword' in request.GET:
            self.search_keyword = request.GET['search_keyword']

        return super(KeywordView, self).get(request=request, args=args, kwargs=kwargs)
