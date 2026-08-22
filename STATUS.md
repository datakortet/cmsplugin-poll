# Status

Updated 2026-08-22.

## Summary

`cmsplugin-poll` is a maintained open-source fork of Antoine Nguyen's original
Django CMS poll plugin. The core feature set is stable and intentionally small:
polls, choices, session-based voting, results, closing, admin integration, and a
Django CMS plugin.

## Verification

- Test suite: 28 import and unit tests.
- Source coverage: 100% of the 144 measured `cmsplugin_poll` statements.
- Locally verified stacks:
  - Python 3.11.9, Django 3.2.24, Django CMS 3.10.1.
  - Python 3.12.8, Django 4.2.30, Django CMS 3.11.11.
- GitHub Actions matrix:
  - Python 3.10, Django 3.2, Django CMS 3.11.
  - Python 3.12, Django 4.2, Django CMS 3.11.

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

- Distribution metadata still identifies the historic 0.3 release and original
  Bitbucket location. This is preserved pending a deliberate fork release.
- A non-null `close_date` currently acts as a closed flag; it is not compared
  with the current time.
- Duplicate-vote prevention is session-based, not tied to an authenticated user.
- Vote increments use a read/change/save sequence and are not yet atomic under
  simultaneous requests.
- The locale catalogs predate the newest messages and should be reviewed before
  the next translation release.
