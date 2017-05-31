# Copyright 2017 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Sphinx extension for pretty-formatting policy docs."""

import os

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils import statemachine
from oslo_config import cfg
from sphinx.util.nodes import nested_parse_with_titles

from oslo_policy import generator


def _indent(text):
    """Indent by four spaces."""
    prefix = ' ' * 4

    def prefixed_lines():
        for line in text.splitlines(True):
            yield (prefix + line if line.strip() else line)

    return ''.join(prefixed_lines())


def _format_policy_rule(rule):
    """Output a definition list-style rule.

    For example:

        ``os_compute_api:servers:create``

            Create a server

            Default::

                rule:admin_or_owner

            Operations:

            - **POST** ``/servers``
    """
    yield '``{}``'.format(rule.name)
    yield ''

    if rule.description:
        for line in statemachine.string2lines(
                rule.description, tab_width=4, convert_whitespace=True):
            yield _indent(line)

        yield ''

    yield _indent('Default::')
    yield ''
    yield _indent(_indent(rule.check_str))

    if hasattr(rule, 'operations'):
        yield ''
        yield _indent('Operations:')
        yield ''
        for operation in rule.operations:
            yield _indent('- **{}** ``{}``'.format(operation['method'],
                                                   operation['path']))

    yield ''


def _format_policy_section(section, rules):
    # The nested_parse_with_titles will ensure the correct header leve is used.
    yield section
    yield '=' * len(section)
    yield ''

    for rule in rules:
        for line in _format_policy_rule(rule):
            yield line


def _format_policy(namespaces):
    policies = generator.get_policies_dict(namespaces)

    for section in sorted(policies.keys()):
        for line in _format_policy_section(section, policies[section]):
            yield line


class ShowPolicyDirective(rst.Directive):

    has_content = False
    option_spec = {
        'config-file': directives.unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        app = env.app

        config_file = self.options.get('config-file')

        # if the config_file option was not defined, attempt to reuse the
        # 'oslo_policy.sphinxpolicygen' extension's setting
        if not config_file and hasattr(env.config,
                                       'policy_generator_config_file'):
            config_file = env.config.policy_generator_config_file

        # If we are given a file that isn't an absolute path, look for it
        # in the source directory if it doesn't exist.
        candidates = [
            config_file,
            os.path.join(app.srcdir, config_file,),
        ]
        for c in candidates:
            if os.path.isfile(c):
                config_path = c
                break
        else:
            self.error('could not find config file in: %s' % str(candidates))

        self.info('loading config file %s' % config_path)

        conf = cfg.ConfigOpts()
        opts = generator.GENERATOR_OPTS + generator.RULE_OPTS
        conf.register_cli_opts(opts)
        conf.register_opts(opts)
        conf(
            args=['--config-file', config_path],
        )
        namespaces = conf.namespace[:]

        result = statemachine.ViewList()
        source_name = '<' + __name__ + '>'
        for line in _format_policy(namespaces):
            result.append(line, source_name)

        node = nodes.section()
        node.document = self.state.document
        nested_parse_with_titles(self.state, result, node)

        return node.children


def setup(app):
    app.add_directive('show-policy', ShowPolicyDirective)
