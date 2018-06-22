import datetime
import json
from opal.core.test import OpalTestCase
from reporting.templatetags import opal_json


class OpalJsonTestCase(OpalTestCase):
    def test_opal_json(self):
        self.assertEqual(
            json.loads(
                opal_json.jsonify({"day": datetime.date(2018, 11, 21)})
            ),
            {"day": "21/11/2018"}

        )
