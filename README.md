This is reporting - an [Opal](https://github.com/openhealthcare/opal) plugin.

# Reports

The Opal Reporting plugin provides developers with a highly extensible method of
creating downloadable reports in [Opal](https://github.com/openhealthcare/opal).

This plugin is **Alpha** software.

Although it aldeady provides significant and useful functionality, it is in active development,
and delvelopers should anticipate backwards-incompatible API changes as part of minor
(x.VERSION.x) releases.

[![Build
Status](https://travis-ci.org/openhealthcare/opal-reporting.png?branch=v0.1)](https://travis-ci.org/openhealthcare/opal-reporting)
[![Coverage Status](https://coveralls.io/repos/github/openhealthcare/opal-reporting/badge.svg?branch=v0.1)](https://coveralls.io/github/openhealthcare/opal-reporting)

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
    description = """Everyone has to have one report that is their first, this one is yours."""

    def generate_report_data(self, *args, **kwargs):
        return [
            ReportFile(
                file_name="some_file.txt", file_data=[['hello']]
            )
        ]
```

Now if you go to "/reporting/#/list" You should see your report listed. Click on this and it should have an option to download your new report.

## Custom Template
Add template to your report, for example

```python
class YourFirstReport(Report):
    slug = "your-first-report"
    display_name = "Your First Report"
    description = """Everyone has to have one report that is their first, this ones yours"""
    template = "my_template"
```

This allows you to put your own template into the front end instead of the default one.
