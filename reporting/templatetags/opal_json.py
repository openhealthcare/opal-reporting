import json
from django import template
from opal.core.serialization import OpalSerializer
register = template.Library()


def jsonify(value):
    return json.dumps(value, cls=OpalSerializer)


register.filter('jsonify', jsonify)
