# Copyright 2014: Mirantis Inc.
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

from rally.benchmark.processing import utils
from rally import exceptions
from tests import test


class ProcessingUtilsTestCase(test.TestCase):

    def test_percentile(self):
        lst = range(1, 101)
        result = utils.percentile(lst, 0.1)
        self.assertEqual(result, 10.9)

    def test_percentile_value_none(self):
        result = utils.percentile(None, 0.1)
        self.assertEqual(result, None)

    def test_percentile_equal(self):
        lst = range(1, 101)
        result = utils.percentile(lst, 1)
        self.assertEqual(result, 100)

    def test_mean(self):
        lst = range(1, 100)
        result = utils.mean(lst)
        self.assertEqual(result, 50.0)

    def test_mean_empty_list(self):
        lst = []
        self.assertRaises(exceptions.InvalidArgumentsException,
                          utils.mean, lst)
