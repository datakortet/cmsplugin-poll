"""Smoke tests for every runtime module in the distribution."""

import importlib

import pytest
from cms.plugin_pool import plugin_pool

from cmsplugin_poll.cms_plugins import CMSPollPlugin


RUNTIME_MODULES = [
    'cmsplugin_poll.admin',
    'cmsplugin_poll.apps',
    'cmsplugin_poll.cms_plugins',
    'cmsplugin_poll.models',
    'cmsplugin_poll.templatetags.poll_tags',
    'cmsplugin_poll.urls',
    'cmsplugin_poll.views',
]


@pytest.mark.parametrize('module_name', RUNTIME_MODULES)
def test_runtime_module_imports(module_name):
    assert importlib.import_module(module_name)


def test_cms_plugin_is_registered():
    assert plugin_pool.get_plugin('CMSPollPlugin') is CMSPollPlugin
