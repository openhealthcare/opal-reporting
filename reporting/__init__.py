"""
Package definition for the reporting OPAL plugin
"""
from reports import Report, ReportFile, ReportOption

from opal.core import celery  # NOQA
__all__ = ["Report", "ReportFile", "ReportOption"]
