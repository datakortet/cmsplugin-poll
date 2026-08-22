=============================
Django CMS simple poll plugin
=============================

.. image:: https://github.com/datakortet/cmsplugin-poll/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/datakortet/cmsplugin-poll/actions/workflows/tests.yml
   :alt: Test status

``cmsplugin-poll`` is a compact poll application and content plugin for
`Django CMS <https://www.django-cms.org/>`_. It provides polls, choices,
session-based voting, result percentages, closing support, translations, and a
Django CMS plugin that can place a selected poll on a page.

The project is maintained as an open-source fork of Antoine Nguyen's original
package. Its intentionally small design has made it useful and understandable
across many generations of Django and Django CMS.


Features
========

* poll and choice editing through the Django admin;
* a Django CMS plugin for placing a poll in a placeholder;
* one vote per poll per browser session;
* poll closing through the admin action;
* vote totals and percentage results;
* French and Norwegian Bokmal translations; and
* named, namespaced URLs for the poll list, detail, vote, and result views.


Installation
============

Install the package and add it to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        # Django and Django CMS applications...
        "cmsplugin_poll",
    ]

Apply the migrations::

    python manage.py migrate

Include the application URLs in the project's root URL configuration::

    from django.urls import include, path

    urlpatterns = [
        path("poll/", include("cmsplugin_poll.urls")),
    ]

Polls and their choices can then be created in the Django admin. Add the
``Simple poll`` plugin to a Django CMS placeholder and select the poll to show.


Compatibility
=============

The GitHub Actions matrix exercises every environment hop in the shared upgrade
record:

====  ================  ==========  ================
Hop   Python            Django      Django CMS
====  ================  ==========  ================
0     3.10              2.2.28      3.7.4
1     3.11              3.2.24      3.10.1
2     3.11              3.2.24      3.11.11
3     3.11              3.2.24      4.1.11
4     3.12              4.2.30      4.1.11
5     3.12              4.2.30      5.0.10
6     3.13              5.2.17      5.0.10
7     3.14              6.1         5.1.1
====  ================  ==========  ================

The older rows preserve valuable evidence that Antoine Nguyen's clear,
well-structured original implementation remains viable across an exceptional
span of framework generations. The newer rows provide early warning for each
planned upgrade destination.


Historical record
=================

Origins: an excellent foundation
--------------------------------

Antoine Nguyen created ``cmsplugin-poll`` in October 2011 for Django CMS 2.2.
The original implementation deserves particular recognition: the first import
was already a coherent, useful package, not merely a prototype. It included the
models, admin integration, CMS plugin, views, URL configuration, templates,
migrations, tests, packaging, and documentation needed for a complete poll
feature.

That clarity and completeness are the main reason the project has endured.
More than a decade of compatibility work has changed framework APIs and
presentation details, but the current data model and application flow remain
immediately recognizable from Antoine's design. The original author chose a
small, direct architecture that subsequent maintainers could understand and
carry forward with confidence. This fork is very grateful for that work and
aims to preserve both its usefulness and its spirit.

Release and maintenance timeline
--------------------------------

* **2011:** Antoine Nguyen published the initial version on Bitbucket. Version
  0.2 followed later that October, together with packaging improvements and the
  BSD license file.
* **2012:** Bertrand Bordage contributed French localization, cleaner code,
  improved styling, and the convenient return-to-page voting flow. Version 0.3
  was released in July.
* **2012-2013:** Erlend Dalen added Norwegian Bokmal localization, Sekizai-aware
  styling, layout refinements, and Django 1.5 compatibility. These were the
  first contributions from the community that later maintained this fork.
* **2017:** The maintained code was upgraded for Django CMS 3.x and moved from
  Mercurial to Git. South migrations were replaced by native Django migrations,
  with careful attention to the table names already used by production sites.
* **2017-2018:** The templates were adapted to a newer dashboard design and
  received import, template, and URL-reversal fixes.
* **2020-2021:** URL routing was updated for newer Django releases, migration
  dependencies were repaired, and the retired South dependency was removed.
* **2022:** A broad compatibility refresh introduced modern Python string
  methods, named URL reversal, current rendering helpers, and consistent
  session/closed-poll state in both views and CMS plugin rendering.
* **2024:** Django 3.2 compatibility, namespaced URLs, and explicit migration
  deletion behavior were completed.
* **2025-2026:** Deprecated Django translation and URL APIs were replaced, code
  quality was refreshed, and the first substantive automated test suite and
  GitHub Actions matrix were added.

Version ``0.8.0`` marks the maintained fork's first deliberate version advance
while retaining Antoine Nguyen's original authorship and the project's
history. The repository history remains the authoritative detailed record.


Development and tests
=====================

Install the test requirements and one documented hop, for example hop 4::

    python -m pip install -r tests/requirements.txt -r tests/hops/hop-4.txt
    python -m pip install --no-deps --editable .

Run the import and unit tests with coverage::

    python -m pytest --cov=cmsplugin_poll --cov-report=term-missing

The suite covers module imports, plugin registration, models, percentages,
namespaced URLs, admin actions, template tags, CMS plugin context, views,
session voting, closed polls, and result rendering.


GitHub Actions and CI Monitor
=============================

``.github/workflows/tests.yml`` runs the complete test suite for pushes, pull
requests, and manual workflow dispatches. It requests only read access to
repository contents.

The canonical ``datakortet/cmsplugin-poll`` repository can optionally report
test results to the CI Monitor dashboard by defining a repository Actions secret
named ``CIMONITOR_INGEST_TOKEN``. Reporting is deliberately isolated from the
tests, is non-blocking, and is attempted only for pushes to ``master`` in that
exact repository.

Forks need no secrets or configuration. Their tests run normally, their missing
secret is not an error, and they never contact the dashboard. Pull requests also
never receive or use the dashboard credential.


License and credit
==================

The package is distributed under the BSD license; see ``COPYING``. Antoine
Nguyen is the original author and architect. Later contributors and the
Datakortet/Norsk Test maintainers have preserved and adapted his strong original
work for newer Django and Django CMS releases.
