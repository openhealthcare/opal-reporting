"""
Urls for the reporting OPAL plugin
"""
from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url('^reporting$', views.ReportIndexView.as_view(), name="report_index"),
    url('^reporting/list$', views.ReportListView.as_view(), name="report_list"),
)
