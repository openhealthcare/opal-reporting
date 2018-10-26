from mock import patch, mock_open
import json

from django.core.urlresolvers import reverse
from django.test import override_settings

from opal.core.test import OpalTestCase
from reporting.tests.reports import SomeReport
from reporting import Report, ReportFile


class ViewsTestCase(OpalTestCase):
    def setUp(self):
        super(ViewsTestCase, self).setUp()
        self.report = SomeReport
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )


class TestListView(ViewsTestCase):
    def test_get(self):
        response = self.client.get(reverse("report_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Some Report", response.content)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("report_list"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            'registration/login.html'
        )


class TestDetailView(ViewsTestCase):
    def get_url(self):
        return reverse(
            "report_detail",
            kwargs={
                "slug": self.report.get_slug(),
            }
        )

    def test_get(self):
        url = self.get_url()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            ['/some', 'reporting/report_detail.html']
        )

    def test_get_login_required(self):
        url = self.get_url()
        self.client.logout()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            'registration/login.html'
        )

    def test_get_templates_when_not_set(self):
        class SomeOtherReport(Report):
            slug = "some-other-report"
            display_name = "Some Other Report"

            def report_options(self):
                return []

        response = self.client.get(reverse("report_detail", kwargs={
            "slug": SomeOtherReport.get_slug()
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            ['reporting/report_detail.html']
        )


class TestIndexView(ViewsTestCase):
    def test_get(self):
        response = self.client.get(reverse("report_index"))
        self.assertEqual(response.status_code, 200)


class TestReportDownLoadView(ViewsTestCase):
    @override_settings(EXTRACT_ASYNC=False)
    def test_get_sync(self):
        url = reverse("report_download", kwargs={
            "slug": self.report.get_slug()
        })
        response = self.client.post(url, dict(criteria=json.dumps({})))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["content-disposition"],
            'attachment; filename="some-report.zip"'
        )

    @override_settings(EXTRACT_ASYNC=False)
    def test_get_sync_params(self):
        url = reverse("report_download", kwargs={
            "slug": self.report.get_slug()
        })
        criteria = dict(something="other")
        with patch.object(self.report, "generate_report_data") as gen_report:
            gen_report.return_value = [
                ReportFile(
                    file_name="some_file.txt", file_data=[['hello']]
                )
            ]
            response = self.client.post(url, dict(criteria=json.dumps(
                criteria
            )))
        call_args = gen_report.call_args
        self.assertEqual(call_args[1]["user"].username, "testuser")
        self.assertEqual(call_args[1]["criteria"], criteria)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["content-disposition"],
            'attachment; filename="some-report_other.zip"'
        )


@patch('reporting.views.AsyncResult')
class TestReportFileView(ViewsTestCase):
    def test_failure(self, AsyncResult):
        AsyncResult().ready.return_value = True
        AsyncResult().successful.return_value = False
        url = reverse("report_file", kwargs={
            "task_id": "100"
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_pending(self, AsyncResult):
        AsyncResult().ready.return_value = False
        url = reverse("report_file", kwargs={
            "task_id": "100"
        })
        response = self.client.get(url)
        self.assertEqual(response.content, "")

    def test_success(self, AsyncResult):
        AsyncResult().ready.return_value = True
        AsyncResult().successful.return_value = True
        AsyncResult().get.return_value = "zip_file_name", "file_context.txt"
        url = reverse("report_file", kwargs={
            "task_id": "100"
        })
        m = mock_open()
        with patch("reporting.views.open", m, create=True):
            response = self.client.get(url)
        self.assertEqual(response.content, "")
        self.assertTrue(response["content-disposition"].startswith(
            'attachment; filename="zip_file_name'
        ))
