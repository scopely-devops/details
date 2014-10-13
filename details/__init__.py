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
import csv
import decimal

from details.costs import Costs


def load(file):
    """
    This function expects a path to a file containing a
    **Detailed billing report with resources and tags**
    report from AWS.

    It returns a ``Costs`` object containing all of the lineitems
    from that detailed billing report
    """
    fp = open(file)
    reader = csv.reader(fp)
    headers = next(reader)
    costs = Costs(headers)
    for line in reader:
        data = {}
        for i in range(0, len(headers)):
            data[headers[i]] = line[i]
        data['UnBlendedCost'] = decimal.Decimal(data['UnBlendedCost'])
        data['BlendedCost'] = decimal.Decimal(data['BlendedCost'])
        costs.add(data)
    fp.close()
    return costs
