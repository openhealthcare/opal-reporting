from opal.core.views import _build_json_response
from reporting import Report
from opal.core.api import LoginRequiredViewset
from opal.core.views import json_response
from celery.result import AsyncResult
from opal.core import celery
from opal.core.views import json_response, _get_request_data
from django.core.urlresolvers import reverse


def async_extract(report_slug, user=None, criteria=None):
    """
    Given the user and the criteria, let's run an async extract.
    """
    from reporting import tasks
    return tasks.extract.delay(report_slug, user=user, criteria=criteria).id


class ReportApi(LoginRequiredViewset):
    base_name = "reporting"
    lookup_field = 'slug'

    def retrieve(self, *args, **kwargs):
        report_cls = Report.get(kwargs["slug"])
        report = report_cls()
        serialised = _build_json_response(report.to_dict())
        return serialised


class ReportTaskApi(LoginRequiredViewset):
    base_name = "reporting-task"
    lookup_field = 'slug'

    def retrieve(self, *args, **kwargs):
        task_id = kwargs['slug']
        result = AsyncResult(id=task_id, app=celery.app)
        return json_response({
            'ready': result.ready()
        })

    def create(self, *args, **kwargs):
        criteria = _get_request_data(self.request)['criteria']
        extract_id = async_extract(
            self.request.query_params["slug"],
            user=self.request.user,
            criteria=criteria
        )
        return json_response({
            'report_status_url': reverse(
                "reporting-task-detail",
                kwargs=dict(slug=extract_id)
            ),
            'report_file_url': reverse(
                "report_file", kwargs=dict(task_id=extract_id)
            ),
        })
