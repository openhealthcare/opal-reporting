"""
Urls for the reporting OPAL plugin
"""
from django.conf.urls import patterns, url
from reporting import views, api

urlpatterns = patterns(
    '',
    url('^reporting$', views.ReportIndexView.as_view(), name="report_index"),
    url(
        '^reporting/list$',
        views.ReportListView.as_view(),
        name="report_list"
    ),
    url(
        '^reporting/api/(?P<slug>[0-9a-z_-]+)$',
        api.ReportApi.as_view({'get': 'retrieve'}),
        name="report_api"
    ),
    url(
        r'^reporting/(?P<slug>[0-9a-z_-]+)/download$',
        views.ReportDownLoadView.as_view(), name="report_download"
    )
)
