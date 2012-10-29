from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from horizon import api, messages, tables
from horizon.models import bills as billsdb
import logging




LOG = logging.getLogger(__name__)

ENABLE = 0
DISABLE = 1


class EditBillLink(tables.LinkAction):
    name='edit'
    verbose_name=_('Edit Bill')
    url = "horizon:admin:bill:update"
    classes = ("ajax-modal", "btn-edit")
    
class CreateBillLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Bill")
    url = "horizon:admin:bill:create"
    classes = ("ajax-modal", "btn-create")

    def allowed(self, request, user):
        if api.keystone_can_edit_user():
            return True
        return False

class DeleteBillsAction(tables.DeleteAction):
    data_type_singular = _("Bill")
    data_type_plural = _("Bills")

    def allowed(self, request, datum):
        if not api.keystone_can_edit_user():
            return False
        return True

    def delete(self, request, obj_id):
       billsdb.objects.filter(id=obj_id).update(deleted=True)

class ToggleEnabled(tables.BatchAction):
    name = "enabled"
    action_present = (_("Enable"), _("Disable"))
    action_past = (_("Enabled"), _("Disabled"))
    data_type_singular = _("Bill")
    data_type_plural = _("Bills")
    classes = ("btn-enable",)

    def allowed(self, request, bill=None):
        self.enabled = True
        if not bill:
            return self.enabled
        self.enabled = bill.enabled
        if self.enabled:
           # bills.objects.filter(id=bill.id).update(enabled=False)
            self.current_present_action = DISABLE
        else:
           # bills.objects.filter(id=bill.id).update(enabled=True)
            self.current_present_action = ENABLE
        return True

    #def update(self, request, bill=None):
        #super(ToggleEnabled, self).update(request, bill)
        #if bill and bill.id == request.bill.id:
        #    self.attrs["disabled"] = "disabled"

    def action(self, request, obj_id):
        if self.enabled:
            billsdb.objects.filter(id=obj_id).update(enabled=True)
            self.current_past_action = DISABLE
        else:
            billsdb.objects.filter(id=obj_id).update(enabled=False)
            self.current_past_action = ENABLE


class BillTable(tables.DataTable):
    STATUS_CHOICES = (
        ("true", True),
        ("false", False)
    )
    id = tables.Column('id', verbose_name=_('Bill ID'))
    name = tables.Column('name', verbose_name=_('Name'))
    payment_type=tables.Column('payment_type',verbose_name=_('Payment Type'))
    order_unit =tables.Column('order_unit',verbose_name=_('Order Unit'))
    order_size =tables.Column('order_size',verbose_name=_('Order Size'))
    price =tables.Column('price',verbose_name=_('Price'))
    enabled = tables.Column('enabled', verbose_name=_('Enabled'),
                            status=True,
                            status_choices=STATUS_CHOICES,
                            empty_value="False")

    class Meta:
        name = "Bill"
        verbose_name = _("Bills")
        row_actions = (EditBillLink,ToggleEnabled, DeleteBillsAction)
        table_actions = (CreateBillLink,DeleteBillsAction,)
