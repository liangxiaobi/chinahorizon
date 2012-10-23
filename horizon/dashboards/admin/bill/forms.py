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

from django.forms import ValidationError
from django.utils.translation import force_unicode, ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables
from horizon import api, exceptions, forms, messages
from horizon.models import bills
from horizon.utils import validators
import datetime
import logging




LOG = logging.getLogger(__name__)


class BaseBillForm(forms.SelfHandlingForm):
    def __init__(self, request, *args, **kwargs):
        super(BaseBillForm, self).__init__(request, *args, **kwargs)
        # Populate tenant choices


class CreateBillForm(BaseBillForm):
    name = forms.CharField(label=_("Name"))
    region = forms.CharField(label=_("Region"))
    payment_type=forms.CharField(label=_("Payment Type"))
    order_unit =forms.CharField(label=_("Order Unit"))
    order_size =forms.IntegerField(label=_("Order Size"))
    price=forms.FloatField(label=_("Price"))
    def __init__(self, *args, **kwargs):
        super(CreateBillForm, self).__init__(*args, **kwargs)

    # We have to protect the entire "data" dict because it contains the
    # password and confirm_password strings.
    @sensitive_variables('data')
    def handle(self, request, data):
        try:
            LOG.info('Creating bill with name "%s"' % data['name'])
            new_bill = bills(name=data['name'],
                             region=data['region'],
                             payment_type=data['payment_type'],
                             order_unit=data['order_unit'],
                             order_size=data['order_size'],
                             price=data['price'],
                             )
            new_bill.save()
            messages.success(request,
                             _('Bill "%s" was successfully created.')
                             % data['name'])
            return new_bill
        except:
            exceptions.handle(request, _('Unable to create bill.'))
            
class UpdateBillForm(BaseBillForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    name = forms.CharField(label=_("Name"))
    region = forms.CharField(label=_("Region"))
    payment_type=forms.CharField(label=_("Payment Type"))
    order_unit =forms.CharField(label=_("Order Unit"))
    order_size =forms.IntegerField(label=_("Order Size"))
    price=forms.FloatField(label=_("Price"))
    enabled=forms.BooleanField(label="Enabled",required = False)
    def __init__(self, request, *args, **kwargs):
        super(UpdateBillForm, self).__init__(request, *args, **kwargs)

        if api.keystone_can_edit_user() is False:
            for field in ('name', 'Region', 'payment_type', 'order_unit','order_size','price'):
                self.fields.pop(field)

    # We have to protect the entire "data" dict because it contains the
    # password and confirm_password strings.
    @sensitive_variables('data')
    def handle(self, request, data):
        failed, succeeded = [], []
        user_is_editable = api.keystone_can_edit_user()
        bill_id=data.pop('id')
        if user_is_editable:
            msg_bits = (_('name'), _('email'))
            try:
                new_bill = bills(id=bill_id,
                                 name=data['name'],
                             region=data['region'],
                             payment_type=data['payment_type'],
                             order_unit=data['order_unit'],
                             order_size=data['order_size'],
                             price=data['price'],
                             enabled=data['enabled']
                             )
                new_bill.save()
                succeeded.extend(msg_bits)
            except:
                failed.append(msg_bits)
                exceptions.handle(request, _('Unable to create bill.'))

        if succeeded:
            messages.success(request, _('Bill has been updated successfully.'))
        if failed:
            failed = map(force_unicode, failed)
            messages.error(request,
                           _('Unable to update %(attributes)s for the bill.')
                             % {"attributes": ", ".join(failed)})
        return True
