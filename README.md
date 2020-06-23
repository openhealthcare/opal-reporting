This is reporting - an [Opal](https://github.com/openhealthcare/opal) plugin.


## ! Important Notice !

This plugin is no longer actively maintiained - as it depends on a version of django that is no longer supported by OPAL


# Reports

The Opal Reporting plugin provides developers with a highly extensible method of
creating downloadable reports in [Opal](https://github.com/openhealthcare/opal).

This plugin is **Alpha** software.

Although it aldeady provides significant and useful functionality, it is in active development,
and delvelopers should anticipate backwards-incompatible API changes as part of minor
(x.VERSION.x) releases.

[![Build
Status](https://travis-ci.org/openhealthcare/opal-reporting.png?branch=v0.2)](https://travis-ci.org/openhealthcare/opal-reporting)
[![Coverage Status](https://coveralls.io/repos/github/openhealthcare/opal-reporting/badge.svg?branch=v0.2)](https://coveralls.io/github/openhealthcare/opal-reporting)

## Contents
* [Introduction: What is a Report?](#introduction-what-is-a-report* * [Quickstart Guide](#quickstart-guide))

## Introduction: What Is A Report?

A report is a cut of data from an Opal application. The reports are downloaded as a zipped file containing one or more csv files.

## Quickstart Guide

In this section we walk you through creating a simple Report.

Pip install opal-reporting from github and add it to your INSTALLED_APPS

Create a report object in your {{ application }}/reports.py. This should look something like the below...

```python
class YourFirstReport(Report):
    slug = "your-first-report"
    display_name = "Your First Report"
    description = """Everyone has to have one report that is their first, this ones yours"""

    def report_options(self):
        return dict(
            criteria=dict(option=1),
            display_name="Option 1"
        )

      def generate_report_data(self, criteria=None, **kwargs):
          option = criteria["option"]
          return [
              ReportFile(
                  file_name="some_file.txt",
                  file_data=option
              )
          ]

```


Now if you go to "/reporting/#/list" You should see your report listed. Click on this and it should have an option to download your new report.

## Custom Option Template
Add template to the report options that appear in the front end.

```python
class YourFirstReport(Report):
    slug = "your-first-report"
    display_name = "Your First Report"
    description = """Everyone has to have one report that is their first, this ones yours"""

    def report_options(self):
        return [dict(
            criteria=dict(option=1),
            template="my_template.html",
            display_month="July",
            display_text="Summer Holiday"
        )]

    # this can just be the same as above
    def generate_report_data...
```

`my_template.html` would then look something like
``` html
  <h1>{{ report_option.display_month }}</h1>
  <h2>{{ report_option.display_text }}</h2>
```
