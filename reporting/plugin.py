"""
Plugin definition for the reporting OPAL plugin
"""
from opal.core import plugins

from reporting import api
from reporting.urls import urlpatterns


class ReportingPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our OPAL application.
    """
    urls = urlpatterns
    javascripts = {
        # Add your javascripts here!
        'opal.reporting': [
            'js/reporting/app.js',
            'js/reporting/controllers/report_detail.js',
            'js/reporting/controllers/report_list.js',
            'js/reporting/services/report_loader.js',
            'js/reporting/services/report.js',
        ]
    }

    apis = (
        ("reporting", api.ReportApi,),
        ("reporting-task", api.ReportTaskApi,),
    )

    def list_schemas(self):
        """
        Return any patient list schemas that our plugin may define.
        """
        return {}

    def roles(self, user):
        """
        Given a (Django) USER object, return any extra roles defined
        by our plugin.
        """
        return {}
