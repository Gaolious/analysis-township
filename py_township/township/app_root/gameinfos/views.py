from django.views import generic

from app_root.gameinfos.models import GameInfo

CURRENT_MENU = 'gameinfo'


class GameInfoListView(generic.ListView):
    template_name = 'gameinfo_list.html'
    model = GameInfo


class GameInfoDetailView(generic.DetailView):
    template_name = 'gameinfo_detail.html'
    model = GameInfo
    pk_url_kwarg = 'gameinfo_pk'
