import functools
import datetime
import os
import tempfile
import zipfile
import csv
import json
from django.core.urlresolvers import reverse

from opal.core import discoverable

import collections


ReportFile = collections.namedtuple('ReportFile', 'file_name file_data')


class ReportOption(object):
    """
    The options as they appear in the template
    """
    template = "reporting/report_option.html"
    critera = {}

    def __init__(self, download_link, **kwargs):
        self.download_link = download_link
        if "display_name" not in kwargs:
            if "template" not in kwargs:
                err = "Either display name or a template is required by Report \
Option"
                raise ValueError(err)

        if "criteria" not in kwargs:
            raise ValueError("ReportOption requires a criteria")
        for k, v in kwargs.items():
            setattr(self, k, v)


class Report(discoverable.DiscoverableFeature):
    module_name = "reports"

    # the template that will be used for the detail view, rendered with the report in the
    # the template as 'object'
    template = None

    # The description displayed in the list view
    description = None
    file_name = ""

    # the text to be displayed if no reports are available
    # the whole template can be override by no_report_templtate
    no_report_text = "Sorry no reports are currently available"

    # the template to be displayed if there are no reports
    no_report_template = None

    def to_dict(self):
        slug = self.__class__.get_slug()
        return dict(
            display_name=self.display_name,
            slug=slug,
            description=self.description,
            create_async_link=self.get_async_create_link()
        )

    def get_download_link(self):
        slug = self.__class__.get_slug()
        return reverse("report_download", kwargs=dict(slug=slug))

    def get_async_create_link(self):
        url = reverse("reporting-task-list")
        return "{0}?slug={1}".format(url, self.__class__.get_slug())

    def generate_report_data(self, user=None, criteria=None):
        # returns a list of ReportFiles, this should be overrode
        raise NotImplementedError(
            "Please implement a way of generating report data"
        )

    def report_options(self):
        raise NotImplementedError(
            "Please implement a way of generating report data"
        )

    def get_zip_name(self, criteria):
        if not criteria:
            return self.slug
        return "{}_{}".format(self.slug, "_".join(criteria.values()))

    def get_report_options(self):
        # returns a list of ReportOptions, this should be overridden
        report_options = self.report_options()
        options = [
            ReportOption(self.get_download_link(), **i) for i in report_options
        ]
        return options

    def write_csv(self, full_file_name, report_data):
        with open(full_file_name, "w") as csv_file:
            writer = csv.writer(csv_file)
            for data in report_data.file_data:
                writer.writerow(data)

    def zip_archive_report_data(self, user=None, criteria=None):
        target_dir = tempfile.mkdtemp()
        target = os.path.join(target_dir, 'extract.zip')

        with zipfile.ZipFile(target, mode='w') as z:
            zipfolder = '{0}.{1}.{2}'.format(
                self.slug, user.username, datetime.date.today()
            )
            os.mkdir(os.path.join(target_dir, zipfolder))
            make_file_path = functools.partial(
                os.path.join, target_dir, zipfolder
            )
            zip_relative_file_path = functools.partial(os.path.join, zipfolder)
            report_data_sequences = self.generate_report_data(
                user=user, criteria=criteria
            )

            for report_data in report_data_sequences:
                full_file_name = make_file_path(report_data.file_name)
                self.write_csv(full_file_name, report_data)
                z.write(full_file_name, zip_relative_file_path(
                    report_data.file_name)
                )

        return self.get_zip_name(criteria), target
