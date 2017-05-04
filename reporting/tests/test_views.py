from opal.core.test import OpalTestCase
from reporting import Report
from django.core.urlresolvers import reverse


class ViewsTestCase(OpalTestCase):
    def setUp(self):
        super(ViewsTestCase, self).setUp()

        class SomeReport(Report):
            slug = "some-report"
            display_name = "Some Report"

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
