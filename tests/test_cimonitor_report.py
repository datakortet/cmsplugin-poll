from scripts.report_to_cimonitor import build_report, read_coverage, read_junit


def test_report_readers_handle_missing_files(tmp_path):
    assert read_junit(tmp_path / 'missing-junit.xml') == {
        'test_count': 0,
        'pass_count': 0,
        'fail_count': 1,
        'runtime': 0.0,
    }
    assert read_coverage(tmp_path / 'missing-coverage.xml') == {
        'coverage': 0.0,
        'loc': 0,
    }


def test_build_report_uses_test_results_and_github_metadata(tmp_path):
    junit = tmp_path / 'junit.xml'
    junit.write_text(
        '<testsuites><testsuite tests="5" failures="1" errors="0" '
        'skipped="1" time="1.25" /></testsuites>',
        encoding='utf-8',
    )
    coverage = tmp_path / 'coverage.xml'
    coverage.write_text(
        '<coverage line-rate="0.875" lines-valid="160" />',
        encoding='utf-8',
    )

    report = build_report({
        'JUNIT_XML': str(junit),
        'COVERAGE_XML': str(coverage),
        'GITHUB_REPOSITORY': 'datakortet/cmsplugin-poll',
        'GITHUB_SERVER_URL': 'https://github.com',
        'GITHUB_RUN_ID': '12345',
        'GITHUB_SHA': 'abcdef',
        'TEST_JOB_STATUS': 'failure',
        'TEST_HOP': '4',
        'TEST_PYTHON_VERSION': '3.12',
        'TEST_DJANGO_VERSION': '4.2.30',
        'TEST_DJANGO_CMS_VERSION': '4.1.11',
    })

    assert report['value'] == '87.5'
    assert report['pipeline_status'] == 'failed'
    assert report['status'] == 'error'
    assert report['pipeline_url'].endswith('/actions/runs/12345')
    assert report['summary'] == {
        'coverage': 87.5,
        'test_count': 5,
        'pass_count': 3,
        'fail_count': 1,
    }
    assert report['details']['loc'] == 160
    assert report['details']['hop'] == '4'
    assert report['details']['django_cms'] == '4.1.11'
    assert report['tag'] == 'github-hop4-py3.12-django4.2.30-cms4.1.11'
