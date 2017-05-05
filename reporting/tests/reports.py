from reporting import Report
from reporting.reports import ReportFile


class SomeReport(Report):
    slug = "some-report"
    display_name = "Some Report"

    def generate_report_data(self, *args, **kwargs):
        return [
            ReportFile(
                file_name="some_file.txt", file_data=[['hello']]
            )
        ]
