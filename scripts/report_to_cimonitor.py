"""Send GitHub Actions test results to CI Monitor when explicitly enabled."""

import json
import os
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree


DEFAULT_INGEST_URL = 'https://cimonitor.vercel.app/api/ingest'


def read_junit(path):
    """Return aggregate test counts and runtime from a JUnit XML report."""
    report_path = Path(path)
    if not report_path.exists():
        return {
            'test_count': 0,
            'pass_count': 0,
            'fail_count': 1,
            'runtime': 0.0,
        }

    root = ElementTree.parse(report_path).getroot()
    suites = [root] if root.tag == 'testsuite' else root.findall('.//testsuite')
    test_count = sum(int(suite.get('tests', 0)) for suite in suites)
    failures = sum(int(suite.get('failures', 0)) for suite in suites)
    errors = sum(int(suite.get('errors', 0)) for suite in suites)
    skipped = sum(int(suite.get('skipped', 0)) for suite in suites)
    runtime = sum(float(suite.get('time', 0)) for suite in suites)

    return {
        'test_count': test_count,
        'pass_count': max(test_count - failures - errors - skipped, 0),
        'fail_count': failures + errors,
        'runtime': runtime,
    }


def read_coverage(path):
    """Return line coverage and source line count from coverage.py XML."""
    report_path = Path(path)
    if not report_path.exists():
        return {'coverage': 0.0, 'loc': 0}

    root = ElementTree.parse(report_path).getroot()
    return {
        'coverage': round(float(root.get('line-rate', 0)) * 100, 2),
        'loc': int(root.get('lines-valid', 0)),
    }


def build_report(environment=None):
    """Build a CI Monitor payload from GitHub and test-report metadata."""
    environment = os.environ if environment is None else environment
    junit = read_junit(environment.get('JUNIT_XML', 'test-results.xml'))
    coverage = read_coverage(environment.get('COVERAGE_XML', 'coverage.xml'))
    repository = environment.get('GITHUB_REPOSITORY', 'datakortet/cmsplugin-poll')
    server_url = environment.get('GITHUB_SERVER_URL', 'https://github.com')
    project_url = '%s/%s' % (server_url.rstrip('/'), repository)
    run_id = environment.get('GITHUB_RUN_ID')
    job_status = environment.get('TEST_JOB_STATUS', 'success')
    pipeline_status = 'success' if job_status == 'success' else 'failed'
    python_version = environment.get('TEST_PYTHON_VERSION', platform.python_version())
    django_version = environment.get('TEST_DJANGO_VERSION', 'unknown')
    django_cms_version = environment.get('TEST_DJANGO_CMS_VERSION', 'unknown')
    hop = environment.get('TEST_HOP', 'unknown')

    return {
        'name': 'cmsplugin_poll',
        'pkg': 'cmsplugin_poll',
        'value': str(coverage['coverage']),
        'created_at': datetime.now(timezone.utc).isoformat(),
        'version': environment.get('GITHUB_SHA'),
        'tag': 'github-hop%s-py%s-django%s-cms%s' % (
            hop,
            python_version,
            django_version,
            django_cms_version,
        ),
        'status': 'ok' if pipeline_status == 'success' else 'error',
        'pipeline_status': pipeline_status,
        'project_url': project_url,
        'pipeline_url': '%s/actions/runs/%s' % (project_url, run_id) if run_id else None,
        'summary': {
            'coverage': coverage['coverage'],
            'test_count': junit['test_count'],
            'pass_count': junit['pass_count'],
            'fail_count': junit['fail_count'],
        },
        'details': {
            'loc': coverage['loc'],
            'runtime': junit['runtime'],
            'hop': hop,
            'python': python_version,
            'django': django_version,
            'django_cms': django_cms_version,
            'platform': sys.platform,
        },
    }


def main():
    """Upload the report, or exit successfully when reporting is not configured."""
    token = os.environ.get('CIMONITOR_INGEST_TOKEN')
    if not token:
        print('CI Monitor reporting skipped: CIMONITOR_INGEST_TOKEN is not configured.')
        return 0

    payload = json.dumps(build_report()).encode('utf-8')
    request = Request(
        os.environ.get('CIMONITOR_INGEST_URL', DEFAULT_INGEST_URL),
        data=payload,
        headers={
            'Authorization': 'Bearer %s' % token,
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    with urlopen(request, timeout=20) as response:
        response_body = response.read().decode('utf-8')
        print('CI Monitor response (%d): %s' % (response.status, response_body))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
