# Copyright (c) 2014 Scopely, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import unittest
import os
import decimal

import killbill


def path(filename):
    return os.path.join(os.path.dirname(__file__), 'data', filename)

COLUMNS = ['InvoiceID',
           'PayerAccountId',
           'LinkedAccountId',
           'RecordType',
           'RecordId',
           'ProductName',
           'RateId',
           'SubscriptionId',
           'PricingPlanId',
           'UsageType',
           'Operation',
           'AvailabilityZone',
           'ReservedInstance',
           'ItemDescription',
           'UsageStartDate',
           'UsageEndDate',
           'UsageQuantity',
           'BlendedRate',
           'BlendedCost',
           'UnBlendedRate',
           'UnBlendedCost',
           'ResourceId',
           'user:Name',
           'user:Role']

SERVICES = ['Amazon Simple Storage Service',
            'Amazon Simple Queue Service',
            'Amazon Elastic Compute Cloud']


class TestCosts(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_costs(self):
        csv_file = path('detailed_with_tags.csv')
        total = killbill.load(csv_file)
        cols = total.columns
        for col in cols:
            self.assertIn(col, COLUMNS)
        for col in COLUMNS:
            self.assertIn(col, cols)
        values = total.values('ProductName')
        for value in values:
            self.assertIn(value, SERVICES)
        for value in SERVICES:
            self.assertIn(value, values)
        self.assertEqual(total.cost, decimal.Decimal('0.08805964'))
        self.assertEqual(total.unblended_cost, decimal.Decimal('0.08805964'))
        self.assertEqual(total.blended_cost, decimal.Decimal('0.08805964'))
        ec2 = total.filter([('ProductName', '.*Elastic Compute.*')])
        self.assertEqual(ec2.cost, decimal.Decimal('0.08800464'))
        s3dt = total.filter([('ProductName', '.*Storage.*'),
                             ('UsageType', '.*DataTransfer.*')])
        self.assertEqual(s3dt.cost, decimal.Decimal('0.00005964'))
