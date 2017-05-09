"""
Views for the reports OPAL Plugin
"""
import datetime
from django.views.generic import ListView, TemplateView, View
from django.conf import settings
from django.http import HttpResponse

from opal.core.views import LoginRequiredMixin
from opal.core.search.views import ajax_login_required_view
from reporting import Report


class ReportIndexView(LoginRequiredMixin, TemplateView):
    """
    Main entrypoint into the reports service.

    """
    template_name = 'reporting/index.html'


class ReportListView(ListView, LoginRequiredMixin):
    template_name = "reporting/report_list.html"

    def get_queryset(self, *args, **kwargs):
        return [i for i in Report.list()]


class ReportDownLoadView(View):
    @ajax_login_required_view
    def get(self, *args, **kwargs):
        report_cls = Report.get(kwargs["slug"])

        fname = report_cls().zip_archive_report_data(self.request.user)
        resp = HttpResponse(open(fname, 'rb').read())
        disp = 'attachment; filename="{0}extract{1}.zip"'.format(
            settings.OPAL_BRAND_NAME, datetime.datetime.now().isoformat())
        resp['Content-Disposition'] = disp
        return resp
