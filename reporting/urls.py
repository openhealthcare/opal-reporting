"""
Urls for the reporting OPAL plugin
"""
from django.conf.urls import patterns, url
from reporting import views, api

urlpatterns = patterns(
    '',
    url('^reporting/$', views.ReportIndexView.as_view(), name="report_index"),
    url(
        '^reporting/list$',
        views.ReportListView.as_view(),
        name="report_list"
    ),
    url(
        '^reporting/detail/(?P<slug>[0-9a-z_-]+)$',
        views.ReportDetailView.as_view(), name='report_detail'
    ),
    url(
        '^reporting/api/(?P<slug>[0-9a-z_-]+)$',
        api.ReportApi.as_view({'get': 'retrieve'}),
        name="report_api"
    ),
    url(
        r'^reporting/result/statut/(?P<task_id>[a-zA-Z0-9-]*)',
        views.ReportAsyncStatusView.as_view(), name='report_status'
    ),
    url(
        r'^reporting/result/download/(?P<task_id>[a-zA-Z0-9-]*)',
        views.ReportFileView.as_view(), name='report_file'
    ),
    url(
        r'^reporting/(?P<slug>[0-9a-z_-]+)/download$',
        views.ReportDownLoadView.as_view(), name="report_download"
    ),
)
