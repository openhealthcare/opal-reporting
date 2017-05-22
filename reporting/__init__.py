"""
Package definition for the reporting OPAL plugin
"""
from reports import Report, ReportFile

from opal.core import celery  # NOQA
__all__ = ["Report", "ReportFile"]
