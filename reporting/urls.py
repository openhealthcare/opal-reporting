"""
Urls for the reports OPAL plugin
"""
from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    '',
    url('^reports$', views.ReportIndexView.as_view(), name="report_index"),
    url('^reports/list$', views.ReportListView.as_view(), name="report_list"),
)
