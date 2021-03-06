# Copyright 2014: The Rally team
# All Rights Reserved.
#
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

from rally.cmd.commands import show
from tests import fakes
from tests import test


class ShowCommandsTestCase(test.TestCase):

    def setUp(self):
        super(ShowCommandsTestCase, self).setUp()
        self.show = show.ShowCommands()
        self.fake_endpoint = {'username': 'fake_username',
                              'password': 'fake_password',
                              'tenant_name': 'fake_tenant_name',
                              'auth_url': 'http://fake.auth.url'}
        self.fake_deploy_id = '7f6e88e0-897e-45c0-947c-595ce2437bee'
        self.fake_clients = fakes.FakeClients()
        self.fake_glance_client = fakes.FakeGlanceClient()
        self.fake_nova_client = fakes.FakeNovaClient()

    @mock.patch('rally.cmd.commands.show.common_cliutils.print_list')
    @mock.patch('rally.cmd.commands.show.cliutils.pretty_float_formatter')
    @mock.patch('rally.cmd.commands.show.utils.Struct')
    @mock.patch('rally.cmd.commands.show.osclients.Clients.glance')
    @mock.patch('rally.cmd.commands.show.db.deployment_get')
    def test_images(self, mock_deployment_get, mock_get_glance,
                    mock_struct, mock_formatter, mock_print_list):
        self.fake_glance_client.images.create('image', None, None, None)
        fake_image = self.fake_glance_client.images.cache.values()[0]
        fake_image.size = 1
        mock_get_glance.return_value = self.fake_glance_client
        mock_deployment_get.return_value = {'endpoints': [self.fake_endpoint]}
        self.show.images(self.fake_deploy_id)
        mock_deployment_get.assert_called_once_with(self.fake_deploy_id)
        mock_get_glance.assert_called_once_with()

        headers = ['UUID', 'Name', 'Size (B)']
        fake_data = [fake_image.id, fake_image.name, fake_image.size]
        mock_struct.assert_called_once_with(**dict(zip(headers, fake_data)))

        fake_formatters = {'Size (B)': mock_formatter()}
        mixed_case_fields = ['UUID', 'Name']
        mock_print_list.assert_called_once_with(
            [mock_struct()],
            fields=headers,
            formatters=fake_formatters,
            mixed_case_fields=mixed_case_fields)

    @mock.patch('rally.cmd.commands.show.common_cliutils.print_list')
    @mock.patch('rally.cmd.commands.show.cliutils.pretty_float_formatter')
    @mock.patch('rally.cmd.commands.show.utils.Struct')
    @mock.patch('rally.cmd.commands.show.osclients.Clients.nova')
    @mock.patch('rally.cmd.commands.show.db.deployment_get')
    def test_flavors(self, mock_deployment_get, mock_get_nova,
                     mock_struct, mock_formatter, mock_print_list):
        self.fake_nova_client.flavors.create()
        fake_flavor = self.fake_nova_client.flavors.cache.values()[0]
        fake_flavor.id, fake_flavor.name, fake_flavor.vcpus = 1, 'm1.fake', 1
        fake_flavor.ram, fake_flavor.swap, fake_flavor.disk = 1024, 128, 10
        mock_get_nova.return_value = self.fake_nova_client
        mock_deployment_get.return_value = {'endpoints': [self.fake_endpoint]}
        self.show.flavors(self.fake_deploy_id)
        mock_deployment_get.assert_called_once_with(self.fake_deploy_id)
        mock_get_nova.assert_called_once_with()

        headers = ['ID', 'Name', 'vCPUs', 'RAM (MB)', 'Swap (MB)', 'Disk (GB)']
        fake_data = [fake_flavor.id, fake_flavor.name, fake_flavor.vcpus,
                     fake_flavor.ram, fake_flavor.swap, fake_flavor.disk]
        mock_struct.assert_called_once_with(**dict(zip(headers, fake_data)))

        fake_formatters = {'RAM (MB)': mock_formatter(),
                           'Swap (MB)': mock_formatter(),
                           'Disk (GB)': mock_formatter()}
        mixed_case_fields = ['ID', 'Name', 'vCPUs']
        mock_print_list.assert_called_once_with(
            [mock_struct()],
            fields=headers,
            formatters=fake_formatters,
            mixed_case_fields=mixed_case_fields)

    @mock.patch('rally.cmd.commands.show.common_cliutils.print_list')
    @mock.patch('rally.cmd.commands.show.utils.Struct')
    @mock.patch('rally.cmd.commands.show.osclients.Clients.nova')
    @mock.patch('rally.cmd.commands.show.db.deployment_get')
    def test_networks(self, mock_deployment_get, mock_get_nova,
                      mock_struct, mock_print_list):
        self.fake_nova_client.networks.create(1234)
        fake_network = self.fake_nova_client.networks.cache.values()[0]
        fake_network.label = 'fakenet'
        fake_network.cidr = '10.0.0.0/24'
        mock_get_nova.return_value = self.fake_nova_client
        mock_deployment_get.return_value = {'endpoints': [self.fake_endpoint]}
        self.show.networks(self.fake_deploy_id)
        mock_deployment_get.assert_called_once_with(self.fake_deploy_id)
        mock_get_nova.assert_called_once_with()

        headers = ['ID', 'Label', 'CIDR']
        fake_data = [fake_network.id, fake_network.label, fake_network.cidr]
        mock_struct.assert_called_once_with(**dict(zip(headers, fake_data)))

        mixed_case_fields = ['ID', 'Label', 'CIDR']
        mock_print_list.assert_called_once_with(
            [mock_struct()],
            fields=headers,
            mixed_case_fields=mixed_case_fields)

    @mock.patch('rally.cmd.commands.show.common_cliutils.print_list')
    @mock.patch('rally.cmd.commands.show.utils.Struct')
    @mock.patch('rally.cmd.commands.show.osclients.Clients.nova')
    @mock.patch('rally.cmd.commands.show.db.deployment_get')
    def test_secgroups(self, mock_deployment_get, mock_get_nova,
                       mock_struct, mock_print_list):
        fake_secgroup = self.fake_nova_client.security_groups.cache.values()[0]
        fake_secgroup.id = 0
        mock_get_nova.return_value = self.fake_nova_client
        mock_deployment_get.return_value = {'endpoints': [self.fake_endpoint]}
        self.show.secgroups(self.fake_deploy_id)
        mock_deployment_get.assert_called_once_with(self.fake_deploy_id)
        mock_get_nova.assert_called_once_with()

        headers = ['ID', 'Name', 'Description']
        fake_data = [fake_secgroup.id, fake_secgroup.name, '']
        mock_struct.assert_called_once_with(**dict(zip(headers, fake_data)))

        mixed_case_fields = ['ID', 'Name', 'Description']
        mock_print_list.assert_called_once_with(
            [mock_struct()],
            fields=headers,
            mixed_case_fields=mixed_case_fields)

    @mock.patch('rally.cmd.commands.show.common_cliutils.print_list')
    @mock.patch('rally.cmd.commands.show.utils.Struct')
    @mock.patch('rally.cmd.commands.show.osclients.Clients.nova')
    @mock.patch('rally.cmd.commands.show.db.deployment_get')
    def test_keypairs(self, mock_deployment_get, mock_get_nova,
                      mock_struct, mock_print_list):
        self.fake_nova_client.keypairs.create('keypair')
        fake_keypair = self.fake_nova_client.keypairs.cache.values()[0]
        fake_keypair.fingerprint = '84:87:58'
        mock_get_nova.return_value = self.fake_nova_client
        mock_deployment_get.return_value = {'endpoints': [self.fake_endpoint]}
        self.show.keypairs(self.fake_deploy_id)
        mock_deployment_get.assert_called_once_with(self.fake_deploy_id)
        mock_get_nova.assert_called_once_with()

        headers = ['Name', 'Fingerprint']
        fake_data = [fake_keypair.name, fake_keypair.fingerprint]
        mock_struct.assert_called_once_with(**dict(zip(headers, fake_data)))

        mixed_case_fields = ['Name', 'Fingerprint']
        mock_print_list.assert_called_once_with(
            [mock_struct()],
            fields=headers,
            mixed_case_fields=mixed_case_fields)
