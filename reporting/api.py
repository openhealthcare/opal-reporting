from opal.core.views import _build_json_response
from reporting import Report
from opal.core.api import LoginRequiredViewset


class ReportApi(LoginRequiredViewset):
    def retrieve(self, *args, **kwargs):
        report_cls = Report.get(kwargs["slug"])
        report = report_cls()
        serialised = _build_json_response(report.to_dict())
        return serialised
