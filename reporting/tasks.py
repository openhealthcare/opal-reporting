from __future__ import absolute_import

from celery import shared_task


@shared_task
def extract(report_slug, user=None, criteria=None):
    from reporting import Report
    import logging
    logging.error("=1=1=1=")
    logging.error(criteria)
    logging.error(criteria.__class__)
    logging.error("=1=1=1=")
    return Report.get(report_slug)().zip_archive_report_data(
        user=user, criteria=criteria
    )
