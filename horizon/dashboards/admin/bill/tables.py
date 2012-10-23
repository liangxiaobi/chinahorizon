import logging

from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _

from horizon import api
from horizon import messages
from horizon import tables


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
    data_type_singular = _("User")
    data_type_plural = _("Users")

    def allowed(self, request, datum):
        if not api.keystone_can_edit_user() or \
                (datum and datum.id == request.user.id):
            return False
        return True

    def delete(self, request, obj_id):
        api.keystone.user_delete(request, obj_id)

class ToggleEnabled(tables.BatchAction):
    name = "enable"
    action_present = (_("Enable"), _("Disable"))
    action_past = (_("Enabled"), _("Disabled"))
    data_type_singular = _("User")
    data_type_plural = _("Users")
    classes = ("btn-enable",)

    def allowed(self, request, user=None):
        self.enabled = True
        if not user:
            return self.enabled
        self.enabled = user.enabled
        if self.enabled:
            self.current_present_action = DISABLE
        else:
            self.current_present_action = ENABLE
        return True

    def update(self, request, user=None):
        super(ToggleEnabled, self).update(request, user)
        if user and user.id == request.user.id:
            self.attrs["disabled"] = "disabled"

    def action(self, request, obj_id):
        if obj_id == request.user.id:
            messages.info(request, _('You cannot disable the user you are '
                                     'currently logged in as.'))
            return
        if self.enabled:
            api.keystone.user_update_enabled(request, obj_id, False)
            self.current_past_action = DISABLE
        else:
            api.keystone.user_update_enabled(request, obj_id, True)
            self.current_past_action = ENABLE


class BillTable(tables.DataTable):
    STATUS_CHOICES = (
        ("true", True),
        ("false", False)
    )
    id = tables.Column('id', verbose_name=_('ID'))
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
        name = "bills"
        verbose_name = _("Bills")
        row_actions = (EditBillLink, ToggleEnabled, DeleteBillsAction)
        table_actions = (CreateBillLink,DeleteBillsAction,)
