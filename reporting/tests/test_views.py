from opal.core.test import OpalTestCase
from django.core.urlresolvers import reverse
from reporting.tests.reports import SomeReport


class ViewsTestCase(OpalTestCase):
    def setUp(self):
        super(ViewsTestCase, self).setUp()
        self.report = SomeReport


class TestListView(ViewsTestCase):
    def test_get(self):
        response = self.client.get(reverse("report_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Some Report", response.content)


class TestIndexView(ViewsTestCase):
    def test_get(self):
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )
        response = self.client.get(reverse("report_index"))
        self.assertEqual(response.status_code, 200)


class TestReportDownLoadView(ViewsTestCase):
    def test_get(self):
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )
        url = reverse("report_download", kwargs={
            "slug": self.report.get_slug()
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
