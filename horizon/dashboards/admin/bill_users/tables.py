from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from horizon import api, messages, tables
from horizon.models import bill_users
import logging




LOG = logging.getLogger(__name__)

ENABLE = 0
DISABLE = 1


class CreateBillUserLink(tables.LinkAction):
    name = "create"
    verbose_name = _("Create User")
    url = "horizon:admin:bill_users:create"
    classes = ("ajax-modal", "btn-create")

    def allowed(self, request, user):
        if api.keystone_can_edit_user():
            return True
        return False


class EditBillUserLink(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit")
    url = "horizon:admin:bill_users:update"
    classes = ("ajax-modal", "btn-edit")


class ToggleEnabled(tables.BatchAction):
    name = "enabled"
    action_present = (_("Enable"), _("Disable"))
    action_past = (_("Enabled"), _("Disabled"))
    data_type_singular = _("User")
    data_type_plural = _("Users")
    classes = ("btn-enable",)

    def allowed(self, request, bill_user=None):
        self.enabled = True
        if not bill_user:
            return self.enabled
        self.enabled = bill_user.enabled
        if self.enabled:
            self.current_present_action = DISABLE
        else:
            self.current_present_action = ENABLE
        return True

    def update(self, request, bill_user=None):
        super(ToggleEnabled, self).update(request, bill_user)
        if bill_user and bill_user.id == request.user.id:
            self.attrs["disabled"] = "disabled"

    def action(self, request, obj_id):
        if self.enabled:
            bill_users.objects.filter(id=obj_id).update(enabled=False)
            self.current_past_action = DISABLE
        else:
            bill_users.objects.filter(id=obj_id).update(enabled=True)
            self.current_past_action = ENABLE


class DeleteBillUsersAction(tables.DeleteAction):
    data_type_singular = _("Bill_User")
    data_type_plural = _("Bill_Users")
    logging.info("DeleteBillUserAction")
    
    def allowed(self, request, datum):
        if datum and datum.username == "admin":
            return False
        return True

    def delete(self, request, obj_id):
        logging.info("delete is processed"+obj_id)
        bill_users.objects.filter(id=obj_id).delete()


class BillUserFilterAction(tables.FilterAction):
    def filter(self, table, bill_users, filter_string):
        """ Really naive case-insensitive search. """
        # FIXME(gabriel): This should be smarter. Written for demo purposes.
        q = filter_string.lower()

        def comp(user):
            if any([q in (user.name or "").lower(),
                    q in (user.email or "").lower()]):
                return True
            return False

        return filter(comp, bill_users)


class BillUsersTable(tables.DataTable):
    STATUS_CHOICES = (
        ("true", True),
        ("false", False)
    )
    id = tables.Column('id', verbose_name=_('User ID'))
    username = tables.Column('username', verbose_name=_('User Name'))
    email = tables.Column('email', verbose_name=_('Email'),
                          filters=[defaultfilters.urlize])
    company= tables.Column('company', verbose_name=_('Company'))
    real_name=tables.Column('real_name', verbose_name=_('Real Name'))
    account=tables.Column('account', verbose_name=_('Account'))
    
    enabled = tables.Column('enabled', verbose_name=_('Enabled'),
                            status=True,
                            status_choices=STATUS_CHOICES,
                            empty_value="False")
    class Meta:
        name = "bill_users"
        verbose_name = _("Bill_Users")
        row_actions = (DeleteBillUsersAction,EditBillUserLink, ToggleEnabled)
        table_actions = (BillUserFilterAction, CreateBillUserLink, DeleteBillUsersAction)
