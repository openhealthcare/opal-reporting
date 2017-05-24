import json
from mock import patch
from django.core.urlresolvers import reverse

from opal.core.test import OpalTestCase
from reporting.tests.reports import SomeReport


class ReportApiTestCase(OpalTestCase):
    def setUp(self):
        super(ReportApiTestCase, self).setUp()
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )

        self.report = SomeReport

    def test_get(self):
        with patch.object(self.report, "to_dict") as to_dict:
            to_dict.return_value = {"some_dict": "yep"}
            url = reverse(
                "reporting-detail", kwargs={"slug": self.report.slug}
            )
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                json.loads(response.content), {"some_dict": "yep"}
            )


class ReportTaskApiTestCase(OpalTestCase):
    def setUp(self):
        super(ReportTaskApiTestCase, self).setUp()
        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )
        self.report = SomeReport()

    @patch("reporting.api.async_extract")
    def test_create(self, async_extract):
        url = self.report.get_async_create_link()
        response = self.client.post(
            url,
            data=json.dumps(dict(criteria=json.dumps({"some": "criteria"}))),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        call_args = async_extract.call_args
        self.assertEqual(call_args[0][0], self.report.get_slug())
        self.assertEqual(call_args[1]["user"].username, "testuser")
        self.assertEqual(call_args[1]["criteria"], {"some": "criteria"})

    @patch("reporting.api.AsyncResult")
    def test_retrieve(self, AsyncResult):
        AsyncResult().ready.return_value = True
        url = reverse("reporting-task-detail", kwargs={
            "slug": "100"
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["ready"], True)
        self.assertEqual(AsyncResult.call_args[1]['id'], '100')
