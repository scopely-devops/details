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
import re

"""
This assumes the headers of the CSV file are in the following order:

* InvoiceID
* PayerAccountId
* LinkedAccountId
* RecordType
* RecordId
* ProductName
* RateId
* SubscriptionId
* PricingPlanId
* UsageType
* Operation
* AvailabilityZone
* ReservedInstance
* ItemDescription
* UsageStartDate
* UsageEndDate
* UsageQuantity
* BlendedRate
* BlendedCost
* UnBlendedRate
* UnBlendedCost
* ResourceId

Followed by any allocation tags in the form:

* user:<tag_name>
"""


class Costs(object):

    def __init__(self, columns):
        self._columns = columns
        self._tags = [c for c in self._columns if c.startswith('user:')]
        self._lineitems = []
        self._blended_cost = 0
        self._unblended_cost = 0
        self._values = {}

    @property
    def columns(self):
        return self._columns

    @property
    def blended_cost(self):
        return self._blended_cost

    @property
    def unblended_cost(self):
        return self._unblended_cost

    @property
    def cost(self):
        return self._unblended_cost

    def add(self, lineitem):
        """
        Add a line item record to this Costs object.
        """
        # Check for a ProductName in the lineitem.
        # If its not there, it is a subtotal line and including it
        # will throw the total cost calculation off.  So ignore it.
        if lineitem['ProductName']:
            self._lineitems.append(lineitem)
            if lineitem['BlendedCost']:
                self._blended_cost += lineitem['BlendedCost']
            if lineitem['UnBlendedCost']:
                self._unblended_cost += lineitem['UnBlendedCost']

    def values(self, column):
        if column not in self._values:
            self._values[column] = set()
            for lineitem in self._lineitems:
                if lineitem[column]:
                    self._values[column].add(lineitem[column])
        return list(self._values[column])

    def filter(self, filters):
        """
        Pass in a list of tuples where each tuple represents one filter.
        The first element of the tuple is the name of the column to
        filter on and the second value is a regular expression which
        each value in that column will be compared against.  If the
        regular expression matches the value in that column, that
        lineitem will be included in the new Costs object returned.

        Example:

            filters=[('ProductName', '.*DynamoDB')]

        This filter would find all lineitems whose ``ProductName``
        column contains values that end in the string ``DynamoDB``.
        """
        subset = Costs(self._columns)
        filters = [(col, re.compile(regex)) for col, regex in filters]
        for lineitem in self._lineitems:
            for filter in filters:
                if filter[1].search(lineitem[filter[0]]) is None:
                    continue
                subset.add(lineitem)
        return subset
