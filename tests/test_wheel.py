"""The py3 wheel CI publishes to pypi.norsktest.xyz builds (INTERN-155).

   Without a py3 file on our index, CI that needs cmsplugin-poll had only
   PyPI's unrelated cmsplugin-poll 0.4 sdist to install, and its setup.py
   ran in the job. .github/workflows/wheel.yml runs this test on Python
   3.13 before it publishes.
"""
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = 'cmsplugin_poll'
#: the files MANIFEST.in and include_package_data put in the package
DATA = ('*.py', '*.html', '*.po', '*.mo')


def version():
    """The version setup.py declares."""
    text = (ROOT / 'setup.py').read_text(encoding='utf-8')
    return re.search(r'''version\s*=\s*["']([^"']+)["']''', text).group(1)


def build_wheel(tmp_path):
    """Build the wheel from a clean copy of the checkout, as CI does.

       setuptools reuses an in-tree build/ directory, so a local build
       could ship files the checkout no longer would.
    """
    source = tmp_path / 'source'
    shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(
        '.git', 'build', 'dist', '*.egg-info', '__pycache__'))
    out = tmp_path / 'dist'
    subprocess.run(
        [sys.executable, '-m', 'pip', 'wheel', '--no-deps', '--quiet',
         '--wheel-dir', str(out), str(source)],
        check=True, env=dict(os.environ, PIP_DISABLE_PIP_VERSION_CHECK='1'))
    wheels = list(out.glob('*.whl'))
    assert len(wheels) == 1, wheels
    return wheels[0]


def test_wheel_is_py3_and_carries_the_whole_package(tmp_path):
    wheel = build_wheel(tmp_path)

    name, wheel_version, python, abi, platform = wheel.stem.split('-')
    assert name == PACKAGE
    assert wheel_version == version()
    assert 'py3' in python.split('.'), wheel.name
    assert (abi, platform) == ('none', 'any')

    with zipfile.ZipFile(wheel) as zf:
        names = set(zf.namelist())
    expected = {
        path.relative_to(ROOT).as_posix()
        for pattern in DATA
        for path in (ROOT / PACKAGE).rglob(pattern)
        if '__pycache__' not in path.parts
    }
    assert expected - names == set()
    # only the package and its metadata: no top-level tests package
    assert {name.split('/', 1)[0] for name in names} == {
        PACKAGE, f'{PACKAGE}-{wheel_version}.dist-info'}
