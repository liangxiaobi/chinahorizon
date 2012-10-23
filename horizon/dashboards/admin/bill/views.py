'''
Created on 2012-10-22

@author:  Lion
@email: 11315889@qq.com

'''
from django.core.urlresolvers import reverse_lazy, reverse
from horizon import api, exceptions, forms, tables
from horizon.dashboards.admin.bill.forms import CreateBillForm, UpdateBillForm
from horizon.dashboards.admin.bill.tables import BillTable
from horizon.models import bills as bill
import operator

    
class UpdateView(forms.ModalFormView):
    form_class = UpdateBillForm
    template_name = 'admin/bill/update.html'
    success_url = reverse_lazy('horizon:admin:bill:index')

    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def get_object(self):
        if not hasattr(self, "_object"):
            try:
                self._object = bill.objects.get(id= self.kwargs['bill_id'])
            except:
                redirect = reverse("horizon:admin:bill:index")
                exceptions.handle(self.request,
                                  _('Unable to update bill.'),
                                  redirect=redirect)
        return self._object

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['bill'] = self.get_object()
        return context

    def get_initial(self):
        _bill = self.get_object()
        return {'id': _bill.id,
                'name': _bill.name,
                'region':_bill.region,
                'payment_type':_bill.payment_type,
                'order_unit':_bill.order_unit,
                'order_size':_bill.order_size,
                'price':_bill.price,
                'enabled':_bill.enabled,
                }

class IndexView(tables.DataTableView):
    table_class = BillTable
    template_name = 'admin/bill/index.html'

    def get_data(self):
        bills = []
        try:
            bills = bill.objects.all();
        except:
            exceptions.handle(self.request,
                              _('Unable to retrieve user list.'))
        return bills

class CreateView(forms.ModalFormView):
    form_class = CreateBillForm
    template_name = 'admin/bill/create.html'
    success_url = reverse_lazy('horizon:admin:bill:index')

    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)


