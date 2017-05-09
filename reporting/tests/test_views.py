from mock import patch, mock_open
import json

from django.core.urlresolvers import reverse
from django.test import override_settings

from opal.core.test import OpalTestCase
from reporting.tests.reports import SomeReport
from reporting import Report


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


class TestDetailView(ViewsTestCase):
    def test_get(self):
        response = self.client.get(reverse("report_detail", kwargs={
            "slug": self.report.get_slug()
        }))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name,
            ['/some', 'reporting/report_detail.html']
        )

    def test_get_templates_when_not_set(self):
        class SomeOtherReport(Report):
            slug = "some-other-report"
            display_name = "Some Other Report"
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
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["content-disposition"].startswith(
            'attachment; filename="reportingextract'
        ))

    @override_settings(EXTRACT_ASYNC=True)
    @patch('reporting.views.async_extract')
    def test_get_async(self, async_extract):
        url = reverse("report_download", kwargs={
            "slug": self.report.get_slug()
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        async_extract.assert_called_once_with(
            self.report.get_slug(), self.user
        )


class TestReportAsyncStatusView(ViewsTestCase):
    @patch('reporting.views.AsyncResult')
    def test_get(self, AsyncResult):
        AsyncResult().ready.return_value = True
        url = reverse("report_status", kwargs={
            "task_id": "100"
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["ready"], True)
        self.assertEqual(AsyncResult.call_args[1]['id'], '100')


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
        AsyncResult().get.return_value = "some_filname.txt"
        url = reverse("report_file", kwargs={
            "task_id": "100"
        })
        m = mock_open()
        with patch("reporting.views.open", m, create=True):
            response = self.client.get(url)
        self.assertEqual(response.content, "")
        self.assertTrue(response["content-disposition"].startswith(
            'attachment; filename="reportingextract'
        ))
