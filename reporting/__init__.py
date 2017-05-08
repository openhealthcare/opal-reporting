"""
Package definition for the reporting OPAL plugin
"""
from reports import Report

from opal.core import celery  # NOQA
__all__ = ["Report"]
