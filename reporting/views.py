"""
Views for the reports Opal Plugin
"""
import datetime
import json

from celery.result import AsyncResult
from django.views.generic import ListView, TemplateView, View, DetailView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from opal.core import celery
from opal.core.views import json_response
from opal.core.search.views import ajax_login_required_view
from rest_framework import status

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


class ReportDetailView(DetailView, LoginRequiredMixin):
    template_name = "reporting/report_detail.html"

    def get_object(self, *args, **kwargs):
        return Report.get(self.kwargs["slug"])()

    def get_template_names(self):
        template_names = super(ReportDetailView, self).get_template_names()
        if self.object.template:
            template_names.insert(0, self.object.template)
        return template_names


class ReportFileView(View):

    @ajax_login_required_view
    def get(self, *args, **kwargs):
        task_id = kwargs['task_id']
        result = AsyncResult(id=task_id, app=celery.app)
        if not result.ready():
            return HttpResponse("")

        if not result.successful():
            return json_response(
                'Nonexistant celery task',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        fname = result.get()
        with open(fname, 'rb') as fh:
            contents = fh.read()
        resp = HttpResponse(contents)
        disp = 'attachment; filename="{0}extract{1}.zip"'.format(
            settings.OPAL_BRAND_NAME, datetime.datetime.now().isoformat())
        resp['Content-Disposition'] = disp
        return resp


class ReportDownLoadView(View):
    @ajax_login_required_view
    def post(self, *args, **kwargs):
        criteria = json.loads(self.request.POST['criteria'])
        report_cls = Report.get(kwargs["slug"])
        fname = report_cls().zip_archive_report_data(
            user=self.request.user,
            criteria=criteria
        )
        resp = HttpResponse(open(fname, 'rb').read())
        disp = 'attachment; filename="{0}extract{1}.zip"'.format(
            settings.OPAL_BRAND_NAME, datetime.datetime.now().isoformat())
        resp['Content-Disposition'] = disp
        return resp
