import functools
import datetime
import os
import tempfile
import zipfile
import csv
from django.core.urlresolvers import reverse

from opal.core import discoverable

import collections


ReportFile = collections.namedtuple('ReportFile', 'file_name file_data')


class Report(discoverable.DiscoverableFeature):
    module_name = "reports"

    # The description displayed in the list view
    description = None
    file_name = ""

    def to_dict(self):
        slug = self.__class__.get_slug()
        return dict(
            display_name=self.display_name,
            slug=slug,
            description=self.description,
            download_link=reverse("report_download", kwargs=dict(slug=slug))
        )

    def generate_report_data(self, user, arguments=None):
        # returns a list of ReportFiles, this should be overrode
        raise NotImplementedError(
            "Please implement a way of generating report data"
        )

    def write_csv(self, full_file_name, report_data):
        with open(full_file_name, "w") as csv_file:
            writer = csv.writer(csv_file)
            for data in report_data.file_data:
                writer.writerow(data)

    def zip_archive_report_data(self, user, arguments=None):
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
            report_data_sequences = self.generate_report_data(user, arguments)

            for report_data in report_data_sequences:
                full_file_name = make_file_path(report_data.file_name)
                self.write_csv(full_file_name, report_data)
                z.write(full_file_name, zip_relative_file_path(
                    report_data.file_name)
                )
        return target
