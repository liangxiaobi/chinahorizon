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
from horizon.models import bill_users
from horizon.utils import validators
import logging




LOG = logging.getLogger(__name__)


class BaseUserForm(forms.SelfHandlingForm):
    def __init__(self, request, *args, **kwargs):
        super(BaseUserForm, self).__init__(request, *args, **kwargs)
        # Populate tenant choices

    def clean(self):
        '''Check to make sure password fields match.'''
        data = super(forms.Form, self).clean()
        if 'password' in data:
            if data['password'] != data.get('confirm_password', None):
                raise ValidationError(_('Passwords do not match.'))
        return data


class CreateUserForm(BaseUserForm):
    username = forms.CharField(label=_("User Name"))
    email = forms.EmailField(label=_("Email"))
    password = forms.RegexField(
            label=_("Password"),
            widget=forms.PasswordInput(render_value=False),
            regex=validators.password_validator(),
            error_messages={'invalid': validators.password_validator_msg()})
    confirm_password = forms.CharField(
            label=_("Confirm Password"),
            required=False,
            widget=forms.PasswordInput(render_value=False))
    company=forms.CharField(label=_("Company Name"),required=False)
    real_name=forms.CharField(label=_("Real Name"),required=False)
    ID_Card=forms.CharField(label=_("ID Card"),required=False)
    mobile=forms.CharField(label=_("Mobile"),required=False)
    qq=forms.CharField(label=_("QQ"),required=False)
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

    @sensitive_variables('data')
    def handle(self, request, data):
        try:
            LOG.info('Creating user with username "%s"' % data['username'])
            new_user = bill_users(
                            username=data['username'],
                            email=data['email'],
                            password=data['password'],
                            company=data['company'],
                            real_name=data['real_name'],
                            ID_Card=data['ID_Card'],
                            mobile=data['mobile'],
                            qq=data['qq'],
                            )
            messages.success(request,
                             _('User "%s" was successfully created.')
                             % data['username'])
            new_user.save()
            return new_user
        except:
            exceptions.handle(request, _('Unable to create user.'))


class UpdateUserForm(BaseUserForm):
    id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    username = forms.CharField(label=_("User Name"))
    email = forms.EmailField(label=_("Email"))
    company=forms.CharField(label=_("Company Name"),required=False)
    real_name=forms.CharField(label=_("Real Name"),required=False)
    ID_Card=forms.CharField(label=_("ID Card"),required=False)
    mobile=forms.CharField(label=_("Mobile"),required=False)
    qq=forms.CharField(label=_("QQ"),required=False)
    enabled=forms.BooleanField(label="Enabled",required = False)

    def __init__(self, request, *args, **kwargs):
        super(UpdateUserForm, self).__init__(request, *args, **kwargs)

        if api.keystone_can_edit_user() is False:
            for field in ('name', 'email', 'password', 'confirm_password'):
                self.fields.pop(field)

    # We have to protect the entire "data" dict because it contains the
    # password and confirm_password strings.
    @sensitive_variables('data')
    def handle(self, request, data):
        failed, succeeded = [], []
        user_is_editable = api.keystone_can_edit_user()
        user_id=data.pop('id')
        if user_is_editable:
            # Update user details
            msg_bits = (_('username'), _('email'))
            try:
                new_user = bill_users.objects.filter(id=user_id).update(
                            username=data['username'],
                            email=data['email'],
                            company=data['company'],
                            real_name=data['real_name'],
                            ID_Card=data['ID_Card'],
                            mobile=data['mobile'],
                            qq=data['qq'],
                            enabled=data['enabled'],
                            )
                succeeded.extend(msg_bits)
            except:
                failed.extend(msg_bits)
                exceptions.handle(request, ignore=True)

        if succeeded:
            messages.success(request, _('User has been updated successfully.'))
        if failed:
            failed = map(force_unicode, failed)
            messages.error(request,
                           _('Unable to update %(attributes)s for the user.')
                             % {"attributes": ", ".join(failed)})
        return True
