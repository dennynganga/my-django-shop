from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# other imports
import uuid


def get_unique_id_str():
    return str(uuid.uuid4())


class Order(models.Model):
    """An order is created when products have been sold.

    **Parameters**:

    number
        The unique order number of the order which is the reference for the
        customer.

    voucher_number, voucher_value, voucher_tax

        Storing this information here assures that we have it all time, even
        when the involved voucher will be deleted.

    requested_delivery_date
        a buyer requested delivery date (e.g. for a florist to deliver flowers on a specific date)

    pay_link
        A link to re-pay the order (e.g. for PayPal)

    """
    number = models.CharField(max_length=30)
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    session = models.CharField(_(u"Session"), blank=True, max_length=100)

    created = models.DateTimeField(_(u"Created"), auto_now_add=True)
    price = models.FloatField(_(u"Price"), default=0.0)
    tax = models.FloatField(_(u"Tax"), default=0.0)

    customer_firstname = models.CharField(_(u"firstname"), max_length=50)
    customer_lastname = models.CharField(_(u"lastname"), max_length=50)
    customer_email = models.CharField(_(u"email"), max_length=50)

    invoice_firstname = models.CharField(_(u"Invoice firstname"), max_length=50)
    invoice_lastname = models.CharField(_(u"Invoice lastname"), max_length=50)
    invoice_company_name = models.CharField(_(u"Invoice company name"), null=True, blank=True, max_length=100)
    invoice_line1 = models.CharField(_(u"Invoice Line 1"), null=True, blank=True, max_length=100)
    invoice_line2 = models.CharField(_(u"Invoice Line 2"), null=True, blank=True, max_length=100)
    invoice_city = models.CharField(_(u"Invoice City"), null=True, blank=True, max_length=100)
    invoice_state = models.CharField(_(u"Invoice State"), null=True, blank=True, max_length=100)
    invoice_code = models.CharField(_(u"Invoice Postal Code"), null=True, blank=True, max_length=100)
    invoice_phone = models.CharField(_(u"Invoice phone"), blank=True, max_length=20)
