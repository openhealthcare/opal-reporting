"""
Plugin definition for the reporting OPAL plugin
"""
from opal.core import plugins, menus

from reporting import api
from reporting.urls import urlpatterns


class ReportingPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our OPAL application.
    """
    urls = urlpatterns
    stylesheets = ["css/reporting.css"]
    javascripts = {
        # Add your javascripts here!
        'opal.services': [
            'js/reporting/services/report_loader.js',
            'js/reporting/services/report.js',
        ],
        'opal.controllers': [
            'js/reporting/controllers/report_detail.js',
            'js/reporting/controllers/report_list.js',
        ],
        'opal.reporting': [
            'js/reporting/app.js',
        ]
    }

    apis = (
        ("reporting", api.ReportApi,),
        ("reporting-task", api.ReportTaskApi,),
    )

    menuitems = [
        menus.MenuItem(
            href="/reporting/#/list", display="Reports", icon="fa fa-file-zip-o",
            activepattern='/reporting', index=1)
    ]

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
