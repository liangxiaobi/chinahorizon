# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2012 Nebula, Inc.
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

"""
Stub file to work around django bug: https://code.djangoproject.com/ticket/7198
"""

from django.db import models

class bill_regions(models.Model):
    name =models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()

class bill_items(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()

class bill_payment_types(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
    interval_unit =models.CharField(max_length=200)
    interval_size = models.IntegerField()
    is_prepaid = models.IntegerField()

class bill_products(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
    region_id=models.IntegerField()
    item_id=models.IntegerField()
    payment_type_id =models.IntegerField()
    order_unit = models.CharField(max_length=200)
    order_size = models.IntegerField()
    price =models.FloatField()
    currency=models.CharField(max_length=200)
    
class bill_journal(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
    region_id=models.IntegerField()
    project_id=models.CharField(max_length=200)
    product_id=models.IntegerField()
    resource_uuid=models.CharField(max_length=200)
    resource_name=models.CharField(max_length=200)
    expires_at =models.DateTimeField()
    status=models.CharField(max_length=200)
    
class bill_purchases(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField()
    updated_at=models.DateTimeField()
    deleted_at=models.DateTimeField()
    deleted = models.IntegerField()
    instance_id =models.IntegerField()
    quantity = models.FloatField()
    line_total = models.FloatField()
    flag = models.IntegerField()
    
class bills(models.Model):
    name = models.CharField(max_length=200)
    create_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(null=True)
    deleted_at=models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    region=models.CharField(max_length=200)
    payment_type =models.CharField(max_length=200)
    order_unit = models.CharField(max_length=200)
    order_size = models.IntegerField()
    price =models.FloatField()
    enabled=models.BooleanField(default=True)
