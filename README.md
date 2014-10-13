[![Build Status](https://travis-ci.org/scopely-devops/killbill.svg?branch=develop)](https://travis-ci.org/scopely-devops/killbill)

details
=======

Utilities to process AWS detailed billing reports.

Installation
------------

The easiest way to install ``details`` is by using ``pip``:

    $ pip install details


Backgroud
---------

The ``details`` package parses the detailed billing reports produced by
AWS.  You can find out more about these reports and how to enable them
for your AWS accounts [here](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/detailed-billing-reports.html).  All testing thus far has been
done using the **Detailed billing report with resources and tags** but the
code should work with any detailed billing report.

Once you have enabled detailed billing on your accounts, AWS will begin to
save these CSV reports in the S3 bucket you have configured.  The ``details``
library assumes you have copied the reports from S3 to your local file
system and uncompressed them if necessary.  The [AWS CLI](https://aws.amazon.com/cli) is a good way to copy the files from S3.

The detailed billing files contain a row (a line item) for every charge on an
account with hourly granularity.  These files can get **huge**.  These tools
currently load an entire months worth of data into memory so if you have a
really large bill this could become impractical.  However, it has been
demonstrated to work reasonably well on detailed billing reports containing
millions of line item records.

Usage
-----

Once you have a detailed billing CSV file available locally, you can load
the file into ``details`` like this:

    >>> import details
    >>> total = details.load('../../bills/123456789012-aws-billing-detailed...')

The variable ``costs`` now points to a ``Cost`` object which contains all of
the line item data for the entire billing file.  Note that depending on the
size of your detailed billing report, this operation can take some time.

Now that you have the ``Cost`` object, you can start by asking it for 
the total cost of the detailed billing report:

    >>> total.cost
    Decimal('1035.7549984289')
    >>>

This number should match (or very nearly match, there are some rounding
errors at times) the total on your bill.  The other thing to note is that
the value returned is a Python Decimal number.  The Decimal type is used
to avoid any further rounding errors within the ``details`` package.
You can use these Decimal numbers as you would normal ints or floats.
Checkout [this](https://docs.python.org/2/library/decimal.html)
for more details on the Decimal type.

In addition to telling you the total cost, the ``Cost`` object has
a few other useful methods.

To find all of the *columns* in CSV data:

    >>> total.columns
    ['InvoiceID',
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

To find all possible values found within a particular column:

    >>> total.values('ProductName')
    ['Amazon Simple Storage Service',
     'Amazon DynamoDB',
     'Amazon Route 53',
     'Route 53 Domain Registration Service',
     'AWS Data Pipeline',
     'Amazon Elastic MapReduce',
     'Amazon RDS Service',
     'Amazon Zocalo',
     'Amazon Simple Queue Service',
     'AWS Support (Business)',
     'Amazon Simple Notification Service',
     'Amazon CloudFront',
     'AWS Support (Developer)',
     'Amazon WorkSpaces',
     'Amazon Redshift',
     'Amazon Elastic Compute Cloud',
     'Amazon ElastiCache',
     'Amazon Kinesis',
     'Amazon CloudSearch',
     'Amazon SimpleDB',
     'Amazon Simple Email Service']

This list will include only the services that actually were used within
this account.

If this report was for a consolidated account, you could find all of the
accounts contained within this report like this:

    >>> total.values('LinkedAccountId')
    ['012345678901',
     '123456789012']
    >>>

The above total represents all of the costs for all services within this
account.  What if you wanted to find the costs just for the EC2 service?
To do this, use the ``filter`` method.  It takes a list of filters where
each filter consists of a column name and a regular expression.  Each value in
that column name is compared to the regular expression and if it matches
it is collected and returned with all of the other matches in another
``Costs`` object.

    >>> ec2 = total.filter([('ProductName', '.*Compute Cloud.*')])
    >>> ec2.cost
    Decimal('315.88505363')
    >>>

So the total cost for EC2 in this account was $315.89.  However, if you
compare that to your bill you will probably find that it doesn't match.
The reason (probably) is that this number includes all Data Transfer
charges incurred as part of the EC2 usage but your monthly bill breaks
data transfer out as a separate line item.  To break out the data transfer
costs:

    >>> data_transfer = ec2.filter([('UsageType', '.*DataTransfer.*')])
    >>> data_transfer.cost
    Decimal('35.45916220')
    >>>

So, if you subtract the data transfer costs from the EC2 costs you should
see the number on your bill.
