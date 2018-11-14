# Copyright (c) 2018 OpenStack Foundation.
# All Rights Reserved.

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock
from oslo_serialization import jsonutils

from oslo_policy import shell
from oslo_policy.tests import base
from oslo_policy.tests import token_fixture


class CheckerTestCase(base.PolicyBaseTestCase):

    SAMPLE_POLICY = '''---
"sample_rule": "role:service"
"sampleservice:sample_rule": ""
'''

    def setUp(self):
        super(CheckerTestCase, self).setUp()
        self.create_config_file("policy.yaml", self.SAMPLE_POLICY)
        self.create_config_file(
            "access.json",
            jsonutils.dumps(token_fixture.SCOPED_TOKEN_FIXTURE))

    @mock.patch("oslo_policy._checks.TrueCheck.__call__")
    def test_pass_rule_parameters(self, call_mock):

        policy_file = open(self.get_config_file_fullname('policy.yaml'), 'r')
        access_file = open(self.get_config_file_fullname('access.json'), 'r')
        apply_rule = None
        is_admin = False
        stdout = self._capture_stdout()

        access_data = token_fixture.SCOPED_TOKEN_FIXTURE["token"]
        target = {
            "project_id": access_data['project']['id']
        }
        access_data['roles'] = [
            role['name'] for role in access_data['roles']]
        access_data['project_id'] = access_data['project']['id']
        access_data['is_admin'] = is_admin

        shell.tool(policy_file, access_file, apply_rule, is_admin)
        call_mock.assert_called_once_with(
            target, access_data, mock.ANY,
            current_rule="sampleservice:sample_rule")

        expected = '''passed: sampleservice:sample_rule
'''
        self.assertEqual(expected, stdout.getvalue())

    @mock.patch("oslo_policy._checks.TrueCheck.__call__")
    def test_pass_rule_parameters_with_custom_target(self, call_mock):
        apply_rule = None
        is_admin = False
        access_data = token_fixture.SCOPED_TOKEN_FIXTURE["token"]
        access_data['roles'] = [
            role['name'] for role in access_data['roles']]
        access_data['project_id'] = access_data['project']['id']
        access_data['is_admin'] = is_admin

        sample_target = {
            "project_id": access_data["project"]["id"],
            "domain_id": access_data["project"]["domain"]["id"]
        }
        self.create_config_file(
            "target.json",
            jsonutils.dumps(sample_target))

        policy_file = open(self.get_config_file_fullname('policy.yaml'), 'r')
        access_file = open(self.get_config_file_fullname('access.json'), 'r')
        target_file = open(self.get_config_file_fullname('target.json'), 'r')
        stdout = self._capture_stdout()

        shell.tool(policy_file, access_file, apply_rule, is_admin,
                   target_file)
        call_mock.assert_called_once_with(
            sample_target, access_data, mock.ANY,
            current_rule="sampleservice:sample_rule")

        expected = '''passed: sampleservice:sample_rule
'''
        self.assertEqual(expected, stdout.getvalue())

    def test_all_nonadmin(self):

        policy_file = open(self.get_config_file_fullname('policy.yaml'), 'r')
        access_file = open(self.get_config_file_fullname('access.json'), 'r')
        apply_rule = None
        is_admin = False
        stdout = self._capture_stdout()

        shell.tool(policy_file, access_file, apply_rule, is_admin)

        expected = '''passed: sampleservice:sample_rule
'''
        self.assertEqual(expected, stdout.getvalue())

    def test_flatten_from_dict(self):
        target = {
            "target": {
                "secret": {
                    "project_id": "1234"
                }
            }
        }
        result = shell.flatten(target)
        self.assertEqual(result, {"target.secret.project_id": "1234"})

    def test_flatten_from_file(self):
        target = {
            "target": {
                "secret": {
                    "project_id": "1234"
                }
            }
        }
        self.create_config_file(
            "target.json",
            jsonutils.dumps(target))
        target_file = open(self.get_config_file_fullname('target.json'), 'r')
        target_from_file = target_file.read()
        result = shell.flatten(jsonutils.loads(target_from_file))
        self.assertEqual(result, {"target.secret.project_id": "1234"})
