from opal.core.test import OpalTestCase
from opal.utils import AbstractBase
from reporting.tests.reports import SomeReport
from reporting import reports


class ReportOptionTestCase(OpalTestCase):
    def test_init_no_display_name_no_template(self):
        with self.assertRaises(ValueError) as ve:
            reports.ReportOption(
                "download_link",
                criteria=dict(something="somethign")
            )

        self.assertEqual(
            str(ve.exception),
            "Either display name or a template is required by Report Option"
        )

    def test_init_no_display_name_but_template(self):
        option = reports.ReportOption(
            "download_link",
            criteria=dict(something="somethign"), template="something.html"
        )
        self.assertTrue(bool(option))

    def test_init_display_name_but_no_template(self):
        option = reports.ReportOption(
            "download_link",
            criteria=dict(something="somethign"), display_name="Something"
        )
        self.assertTrue(bool(option))

    def test_init_no_criteria(self):
        with self.assertRaises(ValueError) as ve:
            reports.ReportOption(
                "download_link",
                template="something.html"
            )

        self.assertEqual(
            str(ve.exception),
            "ReportOption requires a criteria"
        )


class ReportTestCase(OpalTestCase):
    def setUp(self):
        class TestReport(AbstractBase, reports.Report):
            display_name = "display name"
            description = "description"

        self.report = TestReport()

    def test_get_display_name(self):
        self.assertEqual(
            self.report.get_display_name(), "display name"
        )

    def test_get_description(self):
        self.assertEqual(
            self.report.get_description(), "description"
        )

    def test_generate_report_data_fails(self):
        with self.assertRaises(NotImplementedError) as nie:
            reports.Report().generate_report_data()
        self.assertEqual(
            str(nie.exception),
            "Please implement a way of generating report data"
        )

    def test_report_options(self):
        with self.assertRaises(NotImplementedError) as nie:
            reports.Report().report_options()
        self.assertEqual(
            str(nie.exception),
            "Please implement a way of generating report data"
        )

    def test_get_report_options(self):
        report_options = SomeReport().get_report_options()
        self.assertTrue(
            isinstance(report_options[0], reports.ReportOption)
        )
