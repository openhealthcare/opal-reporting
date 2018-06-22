from reporting import Report
from reporting.reports import ReportFile


class SomeReport(Report):
    slug = "some-report"
    display_name = "Some Report"
    template = "/some"

    def generate_report_data(self, *args, **kwargs):
        return [
            ReportFile(
                file_name="some_file.txt", file_data=[['hello']]
            )
        ]

    def report_options(self):
        return [dict(
            criteria=dict(option=1),
            display_name="Option 1"
        )]
