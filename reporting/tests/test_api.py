import json
from mock import patch
from django.core.urlresolvers import reverse

from opal.core.test import OpalTestCase
from reporting.tests.reports import SomeReport


class ApiTestCase(OpalTestCase):
    def setUp(self):
        super(ApiTestCase, self).setUp()

        self.assertTrue(
            self.client.login(
                username=self.user.username, password=self.PASSWORD
            )
        )

        self.report = SomeReport

    def test_get(self):
        with patch.object(self.report, "to_dict") as to_dict:
            to_dict.return_value = {"some_dict": "yep"}
            url = reverse("reporting-detail", kwargs={"slug": self.report.slug})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                json.loads(response.content), {"some_dict": "yep"}
            )
