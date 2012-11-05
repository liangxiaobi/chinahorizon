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

from .forms import CreateUserForm, UpdateUserForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from horizon import api, exceptions, forms, tables
from horizon.dashboards.admin.bill_users.tables import BillUsersTable
from horizon.models import bill_users




class IndexView(tables.DataTableView):
    table_class = BillUsersTable
    template_name = 'admin/bill_users/index.html'

    def get_data(self):
        users = []
        try:
            users = bill_users.objects.all()
        except:
            exceptions.handle(self.request,
                              _('Unable to retrieve user list.'))
        return users


class UpdateView(forms.ModalFormView):
    form_class = UpdateUserForm
    template_name = 'admin/bill_users/update.html'
    success_url = reverse_lazy('horizon:admin:bill_users:index')

    @method_decorator(sensitive_post_parameters('password',
                                                'confirm_password'))
    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def get_object(self):
        if not hasattr(self, "_object"):
            try:
                self._object =bill_users.objects.get(id=self.kwargs['user_id'])
            except:
                redirect = reverse("horizon:admin:bill_users:index")
                exceptions.handle(self.request,
                                  _('Unable to update user.'),
                                  redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['bill_user'] = self.get_object()
        return context

    def get_initial(self):
        user = self.get_object()
        return {'id': user.id,
                'username': user.username,
                'email': user.email,
                'company': user.company,
                'real_name': user.real_name,
                'ID_Card': user.ID_Card,
                'mobile': user.mobile,
                'qq': user.qq,
                'enabled': user.enabled,
                }


class CreateView(forms.ModalFormView):
    form_class = CreateUserForm
    template_name = 'admin/bill_users/create.html'
    success_url = reverse_lazy('horizon:admin:bill_users:index')

    @method_decorator(sensitive_post_parameters('password',
                                                'confirm_password'))
    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)

