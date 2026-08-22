# Status

Updated 2026-08-22.

## Summary

`cmsplugin-poll` is a maintained open-source fork of Antoine Nguyen's original
Django CMS poll plugin. The core feature set is stable and intentionally small:
polls, choices, session-based voting, results, closing, admin integration, and a
Django CMS plugin.

The package version is 0.8.0. Original authorship remains prominently credited
in the package metadata and project documentation.

## Verification

- Test suite: 28 import and unit tests.
- Source coverage: 100% of the 144 measured `cmsplugin_poll` statements.
- All eight documented hop stacks pass locally with clean dependency checks.
- GitHub Actions covers all eight combinations in the shared upgrade record,
  from hop 0 (Python 3.10, Django 2.2.28, Django CMS 3.7.4) through hop 7
  (Python 3.14, Django 6.1, Django CMS 5.1.1).

## CI and reporting

- `.github/workflows/tests.yml` runs on pushes, pull requests, and manual
  dispatches with read-only repository permissions.
- Optional CI Monitor reporting is limited to canonical `master` pushes from
  `datakortet/cmsplugin-poll`.
- The dashboard token is available only to the reporting step. Forks and pull
  requests run the tests without receiving it or contacting CI Monitor.
- Reporting is a successful no-op if `CIMONITOR_INGEST_TOKEN` is not configured.
- Dashboard reporting is non-blocking, so an ingest outage cannot fail the test
  job.

## Known limitations

- Distribution metadata still retains the original Bitbucket URL as historical
  provenance; the canonical fork URL should be selected before publication.
- A non-null `close_date` currently acts as a closed flag; it is not compared
  with the current time.
- Duplicate-vote prevention is session-based, not tied to an authenticated user.
- Vote increments use a read/change/save sequence and are not yet atomic under
  simultaneous requests.
- The locale catalogs predate the newest messages and should be reviewed before
  the next translation release.
