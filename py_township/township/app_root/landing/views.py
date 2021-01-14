from django.views import generic

CURRENT_MENU = 'dashboard'


class DashboardView(generic.TemplateView):
    active_side_menu = CURRENT_MENU
    template_name = 'ts_dashboard.html'
