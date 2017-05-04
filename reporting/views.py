"""
Views for the reports OPAL Plugin
"""
from opal.core.views import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from reports import Report


class ReportIndexView(LoginRequiredMixin, TemplateView):
    """
    Main entrypoint into the reports service.

    """
    template_name = 'report/index.html'


class ReportListView(ListView, LoginRequiredMixin):
    template_name = "report/report_list.html"

    def get_queryset(self, *args, **kwargs):
        return [i for i in Report.list()]
