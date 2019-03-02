import logging
import re
from collections.__init__ import namedtuple

from decimal import Decimal
from django.core import exceptions
from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from oscar.apps.address.abstract_models import AbstractShippingAddress
from oscar.apps.order.abstract_models import AbstractLine, AbstractOrderNote, AbstractOrder

from apps.address.models import State, District, Subdistrict, Village
from apps.payment.constants import CARD_TYPE, BINS

log = logging.getLogger('jimshoney')

STATUS_CANCELED = 'Canceled'
STATUS_SHIPPED = 'Shipped'
STATUS_COMPLETED = 'Completed'


class OrderNote(AbstractOrderNote):
    old_status = models.CharField(max_length=32, null=True, blank=True)
    new_status = models.CharField(max_length=32, null=True, blank=True)


class Order(AbstractOrder):

    @property
    def ipay_cost(self):
        source_type = self.sources.last().source_type
        percentage_fee = self.total_incl_tax * source_type.total_percent_fee
        return round(percentage_fee + source_type.total_bank_fee + source_type.total_amount_fee, 2)

    @property
    def tax_vat(self):
        source_type = self.sources.last().source_type
        return round(((source_type.total_bank_fee + source_type.total_amount_fee) * 10) / 100, 2)

    @property
    def tax_pph23(self):
        return round((self.tax_vat * 2) / 100, 2)

    @property
    def total_ipay_cost(self):
        return round(self.ipay_cost + self.tax_vat - self.tax_pph23, 2)

    @property
    def gdn_fee(self):
        return Decimal(settings.GDN_FEE)

    @property
    def total_gdn_fee(self):
        return round((self.total_incl_tax * self.gdn_fee) / 100, 2)

    @property
    def total_income(self):
        return round(self.total_incl_tax - self.total_ipay_cost - self.total_gdn_fee, 2)

    @property
    def voucher(self):
        return self.discounts.filter(voucher_id__isnull=False).first()

    @property
    def basket_total_incl_tax_before_discount(self):
        """
        Return basket total including tax before discount
        """
        return self.total_incl_tax - self.shipping_before_discounts_incl_tax

    @property
    def total_before_voucher(self):
        return self.basket_total_incl_tax_before_discount + (self.voucher.amount if self.voucher else 0)

    @property
    def kgx_fee(self):
        if self.has_shipping_discounts:
            return self.shipping_before_discounts_incl_tax
        else:
            return self.shipping_incl_tax


class Line(AbstractLine):
    # Price information after discounts are applied
    line_price_after_discounts_incl_tax = models.DecimalField(
        _("Price after discounts (inc. tax)"),
        decimal_places=2, max_digits=12, default=0)
    line_price_after_discounts_excl_tax = models.DecimalField(
        _("Price after discounts (excl. tax)"),
        decimal_places=2, max_digits=12, default=0)


class ShippingAddress(AbstractShippingAddress):
    line1 = models.CharField(_("Alamat"), max_length=255)
    province = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, verbose_name=_("Provinsi"))
    regency_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True,
                                         verbose_name=_("Kota/Kabupaten"))
    subdistrict = models.ForeignKey(Subdistrict, on_delete=models.SET_NULL, null=True, verbose_name=_("Kecamatan"))
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, verbose_name=_("Desa/Kelurahan"))

    country = models.ForeignKey(
        'address.Country',
        on_delete=models.CASCADE,
        verbose_name=_("Country"), default="ID")

    base_fields = hash_fields = ['salutation', 'complete_address', 'postcode', 'phone_number']

    def get_field_values(self, fields):
        field_values = []
        for field in fields:
            if field == 'title':
                value = self.get_title_display()
            elif field == 'country':
                try:
                    value = self.country.printable_name
                except exceptions.ObjectDoesNotExist:
                    value = ''
            elif field == 'salutation':
                value = self.salutation
            elif field == 'complete_address':
                value = f'{self.line1}, {self.village.name}, {self.subdistrict.name}, \
                {self.regency_district.name} - {self.province.name}'
            elif field == 'phone_number':
                value = 'Telp: ' + str(self.phone_number) if self.phone_number else 'Telp: -'
            elif field == 'province':
                value = self.province.name
            elif field == 'regency_district':
                value = self.regency_district.name
            elif field == 'subdistrict':
                value = self.subdistrict.name
            elif field == 'village':
                value = self.village.name
            else:
                value = getattr(self, field)
            field_values.append(value)
        return field_values


    def get_address_field_values(self, fields):
        field_values = [f.strip() for f in self.get_field_values(fields) if f]
        return field_values

    def active_address_fields(self):
        return self.get_address_field_values(self.base_fields)


class OrderReport(TimeStampedModel):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, default="")
    number = models.CharField(_("Order number"), max_length=128, db_index=True, unique=True)
    date_placed = models.DateTimeField(db_index=True, default=None, blank=True, null=True)
    order_amount = models.DecimalField(_("Order Amount"), decimal_places=2, default=0, max_digits=12)
    shipping_cost = models.DecimalField(_("Shipping_cost"), decimal_places=2, default=0, max_digits=12)
    product_promo = models.DecimalField(_("Product Promo"), decimal_places=2, default=0, max_digits=12)
    shipping_promo = models.DecimalField(_("Shipping Promo"), decimal_places=2, default=0, max_digits=12)
    total_order = models.DecimalField(_("Total Order"), decimal_places=2, default=0, max_digits=12)
    source_type = models.ForeignKey('payment.SourceType', on_delete=models.CASCADE, default="")
    payment_method = models.CharField(_("Payment Method"), max_length=128)
    percent_fee = models.DecimalField(_("Percent Fee"), max_digits=6, default=0, decimal_places=2)
    gdn_percent_fee = models.DecimalField(_("GDN Percent Fee"), max_digits=6, default=0, decimal_places=2)
    bank_fee = models.DecimalField(_("Bank Fee"), max_digits=12, default=0, decimal_places=2)
    gdn_bank_fee = models.DecimalField(_("GDN Bank Fee"), max_digits=12, default=0, decimal_places=2)
    amount_fee = models.DecimalField(_("Amount Fee"), max_digits=12, default=0, decimal_places=2)
    gdn_amount_fee = models.DecimalField(_("GDN Amount Fee"), max_digits=12, default=0, decimal_places=2)
    ipay_cost = models.DecimalField(_("Ipay Cost"), max_digits=12, default=0, decimal_places=2)
    tax_vat = models.DecimalField(_("Tax VAT"), max_digits=12, default=0, decimal_places=2)
    tax_pph23 = models.DecimalField(_("Tax PPH23"), max_digits=12, default=0, decimal_places=2)
    total_ipay_cost = models.DecimalField(_("Total IPAY Cost"), max_digits=12, default=0, decimal_places=2)
    gdn_fee_percent = models.DecimalField(_("GDN Fee Percent"), max_digits=6, default=0, decimal_places=2)
    total_gdn_fee = models.DecimalField(_("Total GDN Fee"), max_digits=12, default=0, decimal_places=2)
    income_ipay = models.DecimalField(_("Income IPay"), max_digits=12, default=0, decimal_places=2)

    @property
    def total_percent_fee(self):
        return self.percent_fee + self.gdn_percent_fee

    @property
    def total_bank_fee(self):
        return self.bank_fee + self.gdn_bank_fee

    @property
    def total_amount_fee(self):
        return self.amount_fee + self.gdn_amount_fee


CardDetail = namedtuple('CardDetail', ['bank_name', 'card_type'])


def get_card_type(masked_card):
    for card_type in CARD_TYPE:
        match = re.search(card_type.get("pattern"), masked_card)
        if match:
            return card_type.get("type").title()

    return None


def get_bank_name(masked_card):
    bank_code, last_digit = masked_card.split('-')
    for bank in BINS:
        if int(bank_code) in bank.get("bins"):
            return bank.get("bank").upper()
    return None


def bank_name_from_mask(masked_card):
    """
    :param masked_card: "410505-2148"
    :return: CardDetail
    """
    card_type = get_card_type(masked_card)
    bank_name = get_bank_name(masked_card)

    return CardDetail(bank_name, card_type)

from oscar.apps.order.models import *  # noqa isort:skip
