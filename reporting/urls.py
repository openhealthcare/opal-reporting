"""
Urls for the reporting OPAL plugin
"""
from django.conf.urls import patterns, url
from reporting import views

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
        r'^reporting/result/download/(?P<task_id>[a-zA-Z0-9-]*)',
        views.ReportFileView.as_view(), name='report_file'
    ),
    url(
        r'^reporting/(?P<slug>[0-9a-z_-]+)/download$',
        views.ReportDownLoadView.as_view(), name="report_download"
    ),
)
