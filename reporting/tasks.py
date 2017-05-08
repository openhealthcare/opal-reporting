from __future__ import absolute_import

from celery import shared_task


@shared_task
def extract(report_slug, user=user, criteria=None):
    from reporting import Report
    return Report.get(report_slug)().zip_archive_report_data(
        user=user, criteria=criteria
    )
