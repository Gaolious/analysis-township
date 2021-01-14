from django.views import generic

from core.views.cursor_pagination import CursorPaginator


class CursorPaginationMixin(generic.ListView):
    paginator_class = CursorPaginator
    paginate_by = 10
    ordering = ('-pk',)

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset,
            page_size,
            self.ordering
        )
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg)

        page = paginator.page(page)
        return (paginator, page, page.object_list, page.has_other_pages())


    def get_paginator(self, queryset, page_size, ordering, allow_empty_first_page=True, ** kwargs):
        return self.paginator_class(
            queryset,
            page_size,
            ordering
        )